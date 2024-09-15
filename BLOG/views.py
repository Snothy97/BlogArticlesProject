from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogArticle
from .forms import BlogArticleForm, CommentForm
from django.http import JsonResponse

@login_required
def blog_page(request):
    return render(request, 'blog.html')


@login_required
def list_articles(request):
    articles = BlogArticle.objects.all()
    return render(request, 'blog/article.html', {'articles': articles})

@login_required
def article_detail(request, pk):
    article = get_object_or_404(BlogArticle, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', pk=pk)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/article_detail.html', {
        'article': article,
        'comment_form': comment_form
    })

@csrf_exempt
@login_required  # Ensures that only logged-in users can create articles
def create_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        file = request.FILES.get('file')
        author = request.user  # Use the currently logged-in user as the author

        if not title or not content :
            return JsonResponse({'status': 'error', 'error': 'Title and content are required'}, status=400)

        article = BlogArticle(title=title, content=content, author=author)
        if file:
            article.file = file

        try:
            article.save()
            response_data = {
                'status': 'success',
                'message': 'Article created successfully'
            }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'error': 'Invalid request method'}, status=400)

@login_required
def update_article(request, article_id):
    article = get_object_or_404(BlogArticle, id=article_id)
    if request.method == 'POST':
        form = BlogArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Article updated successfully', 'article': {
                'id': article.id, 'title': article.title, 'content': article.content
            }})
        return JsonResponse({'status': 'error', 'message': 'Form is invalid'}, status=400)


@login_required
def delete_article(request, article_id):
    if request.method == 'DELETE':
        article = get_object_or_404(BlogArticle, pk=article_id)
        
        if request.user != article.author:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        
        article.delete()
        return JsonResponse({'status': 'success', 'message': 'Article deleted successfully'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
