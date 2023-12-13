from django.db import models
from .expense import Expense


class ExpenseComment(models.Model):
    expense = models.ForeignKey(Expense,
                                 on_delete=models.CASCADE,
                                 related_name='expense_comment')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self) -> str:
        return f'Comment by {self.name} on {self.expense}'