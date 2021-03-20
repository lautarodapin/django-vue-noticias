from django.db import models
from django.db.models.indexes import Index
from users.models import User


class Todo(models.Model):
    class Meta:
        verbose_name = "ToDo"
        verbose_name_plural = "ToDos"
        indexes = [
            Index(fields=["user", "is_done"])
        ]
        ordering = ["-created_at"]
    mod_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos", null=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    is_done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Todo(id={self.pk}, title={self.title}, is_done={self.is_done}, user={self.user})"