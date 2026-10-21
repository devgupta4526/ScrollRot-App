"""URL configuration for scrollrot_api project.

Complete versioned v1 REST API routes adhering to docs/24_API_CONTRACT.md.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import HealthCheckView, APIRootView
from accounts.views import (
    RegisterView,
    LoginView,
    LogoutView,
    MeView,
    SharingConsentView,
    UserSearchView,
)
from friendships.views import (
    FriendRequestListCreateView,
    AcceptFriendRequestView,
    DeclineFriendRequestView,
    FriendsListView,
    RemoveFriendView,
    BlockListCreateView,
    UnblockUserView,
)
from battles.views import (
    BattleListCreateView,
    BattleDetailView,
    BattleJoinView,
    BattleLeaveView,
    BattleLeaderboardView,
    ScoreUpsertView,
)

v1_patterns = [
    # Discovery & Health
    path("", APIRootView.as_view(), name="api-root"),
    path("health/", HealthCheckView.as_view(), name="api-health"),
    # Authentication & Profile
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("auth/logout/", LogoutView.as_view(), name="auth-logout"),
    path("me/", MeView.as_view(), name="user-profile"),
    path("me/sharing-consent/", SharingConsentView.as_view(), name="sharing-consent"),
    # User Search
    path("users/search/", UserSearchView.as_view(), name="users-search"),
    # Friend Requests & Friendships
    path("friend-requests/", FriendRequestListCreateView.as_view(), name="friend-requests"),
    path("friend-requests/<uuid:pk>/accept/", AcceptFriendRequestView.as_view(), name="friend-request-accept"),
    path("friend-requests/<uuid:pk>/decline/", DeclineFriendRequestView.as_view(), name="friend-request-decline"),
    path("friends/", FriendsListView.as_view(), name="friends-list"),
    path("friends/<uuid:pk>/", RemoveFriendView.as_view(), name="friend-remove"),
    # User Blocks
    path("blocks/", BlockListCreateView.as_view(), name="blocks-list-create"),
    path("blocks/<uuid:pk>/", UnblockUserView.as_view(), name="block-remove"),
    # Battles & Leaderboards
    path("battles/", BattleListCreateView.as_view(), name="battles-list-create"),
    path("battles/join/", BattleJoinView.as_view(), name="battle-join"),
    path("battles/<uuid:pk>/", BattleDetailView.as_view(), name="battle-detail"),
    path("battles/<uuid:pk>/leave/", BattleLeaveView.as_view(), name="battle-leave"),
    path("battles/<uuid:pk>/leaderboard/", BattleLeaderboardView.as_view(), name="battle-leaderboard"),
    path("battles/<uuid:pk>/scores/<str:local_date>/<str:platform>/", ScoreUpsertView.as_view(), name="battle-score-upsert"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", HealthCheckView.as_view(), name="top-health"),
    path("api/v1/", include((v1_patterns, "v1"))),
]
