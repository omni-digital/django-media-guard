from django.conf.urls import url

from example.views import DownloadableFileView, ItemDetail, ItemList


urlpatterns = [
    url(r"^$", ItemList.as_view(), name="item_list"),
    url(r"^(?P<pk>\d+)/$", ItemDetail.as_view(), name="item_detail"),
    url(r"^downloads/(?P<pk>\d+)/$", DownloadableFileView.as_view(), name="download"),
]
