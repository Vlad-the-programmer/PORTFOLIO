from .models import Comment


class GetCommentObjectMixin():
        
    def get_object(self):
        pk_ = self.kwargs.get('pk', '')
        try:
            comment = Comment.objects.get(pk=pk_)
        except Comment.DoesNotExist:
            comment = None

        return comment