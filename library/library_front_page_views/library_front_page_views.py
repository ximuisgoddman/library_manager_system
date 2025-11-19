from django.shortcuts import render
from django.urls import reverse

from article.models import ArticlePost
from online_books.models import OnlineBooksModel, BookShelfModel
from online_song.models import OnlineSongModel, MyFavoriteMusic


def library_front_page(request):
    featured_books = OnlineBooksModel.objects.order_by('-update_time')[:4]
    featured_songs = OnlineSongModel.objects.order_by('-update_time')[:4]
    featured_articles = (
        ArticlePost.objects.select_related('author')
        .order_by('-total_views', '-created')[:3]
    )

    games_showcase = [
        {
            "title": "魂斗罗 · 霓虹反击",
            "description": "原创三段关卡 + 合成音效，重温街机火力。",
            "url": reverse('contra'),
            "icon": "fas fa-crosshairs",
        },
        {
            "title": "暴力摩托 · Neo Ride",
            "description": "赛博霓虹高速公路，极速冲刺打破记录。",
            "url": reverse('moto_racer'),
            "icon": "fas fa-motorcycle",
        },
        {
            "title": "俄罗斯方块",
            "description": "经典消除闯关，保持节奏拿高分。",
            "url": reverse('tetris'),
            "icon": "fas fa-th-large",
        },
        {
            "title": "吃豆人",
            "description": "迷宫追逐大战，考验策略与手速。",
            "url": reverse('pacman'),
            "icon": "fas fa-dot-circle",
        },
    ]

    library_metrics = {
        "book_count": OnlineBooksModel.objects.count(),
        "song_count": OnlineSongModel.objects.count(),
        "article_count": ArticlePost.objects.count(),
        "game_count": len(games_showcase),
    }

    user_snapshot = None
    if request.user.is_authenticated:
        user_snapshot = {
            "bookshelf": BookShelfModel.objects.filter(
                book_shelf_user_id=request.user
            ).count(),
            "favorite_music": MyFavoriteMusic.objects.filter(
                favorite_music_user_id=request.user
            ).count(),
            "articles": ArticlePost.objects.filter(author=request.user).count(),
        }

    context = {
        "featured_books": featured_books,
        "featured_songs": featured_songs,
        "featured_articles": featured_articles,
        "games_showcase": games_showcase,
        "library_metrics": library_metrics,
        "user_snapshot": user_snapshot,
    }

    return render(request, 'user_front_page/front_page.html', context)
