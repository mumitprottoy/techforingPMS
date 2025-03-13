from django.db import models
from django.core import exceptions
from . import messages as msg


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def authenticate(
        cls, username: str, password: str) -> tuple[bool, str]:
        user = cls.objects.filter(username=username)
        if user is not None:
            if user.password == password:
                return True, msg.SUCCESS
            return False, msg.WRONG_PASSWORD
        return False, msg.USER_DOES_NOT_EXIST
            
    def __str__(self) -> str:
        return self.username


class Project(models.Model):
    """
    The project name HAS TO BE unique since being able to 
    identify a project only by its id is impractical.
    """
    name = models.CharField(max_length=100, unique=True) 
    description = models.TextField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # A feature to change the project owner if necessary
    def change_owner(self, user: User) -> None:
        self.owner = user
        self.save() 

    # A method to lookup if this project has an admin, returns bool
    @property
    def has_admin(self) -> bool:
        return self.members.filter(
            role=self.members.model.ADMIN).exists()

    def __str__(self) -> str:
        return self.name
    

class ProjectMember(models.Model):
    ADMIN = 'Admin'; MEMBER = 'Member'
    ROLE_CHOICES = ((ADMIN, ADMIN), (MEMBER, MEMBER))
    
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='members')
    """
    setting the related name to "projects" is useful because it's practical
    to be needed to see which projects this user is assigned to.
    it can be achieved by user.projects.all()
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    role = models.CharField(
        max_length=6, choices=ROLE_CHOICES, default=MEMBER)
    
    """
    It is practical to have a method to change the current admin
    or assign someone as admin if there was none already.
    This method also automatically changes the role of previous admin to
    member (if exists)
    """
    def make_admin(self) -> None:
        # this is only updated if this user not already an admin
        if self.role != self.__class__.ADMIN:
            # changes the role of previous admin to member (if exists)
            self.__class__.objects.filter(
                project=self.project, role=self.__class__.ADMIN).update(
                    role=self.__class__.MEMBER)
            # assigns this user as the new admin
            self.role = self.__class__.ADMIN
            self.save()
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        # A member cannot appear more than once in the same project
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'user'],
                name='unique_member_within_project')
        ]


class Task(models.Model):
    TO_DO = 'To Do'; IN_PROG = 'In Progress'; DONE = 'Done'
    STATUS_CHOICES = ((TO_DO, TO_DO), (IN_PROG, IN_PROG), (DONE, DONE))
    LOW = 'Low'; MED = 'Medium'; HIGH = 'High'
    PRIORITY_CHOICES = ((LOW, LOW), (MED, MED), (HIGH, HIGH))
    
    # A task within a project should be unique
    title = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=TO_DO)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default=HIGH)
    # A task within a project should be assigned to its members, not to other users
    assigned_to = models.ForeignKey(
        ProjectMember, on_delete=models.CASCADE, related_name='assigned_tasks') # get all tasks assigned to a member by member.assigned_tasks.all()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks') # get all tasks within a project by project.tasks.all()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        """
        It must be ensured that the ProjectMember is from the right Project
        before saving to DB, else raise an exception
        """
        if self.assigned_to.project != self.project:
            raise exceptions.ValidationError('This user is not a member of this project.')
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
    

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
