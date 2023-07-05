import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")
    email = django_filters.CharFilter(lookup_expr="icontains")
    first_name = django_filters.CharFilter(lookup_expr="icontains")
    is_staff = django_filters.BooleanFilter()
    is_superuser = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()
    search = django_filters.CharFilter(method="custom_user_search_filter")

    class Meta:
        db_table = User
        fields = (
            "username",
            "email",
            "first_name",
            "is_staff",
            "is_superuser",
            "is_active",
            "search",
        )

    def custom_user_search_filter(self, queryset, name, value):
        queryset = queryset.filter(
            Q(username__icontains=value)
            | Q(first_name__icontains=value)
            | Q(email__icontains=value)
            | Q(last_name__icontains=value)
        )
        if not queryset.exists():
            return queryset.none()
        return queryset
