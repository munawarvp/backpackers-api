from django.urls import path
from .views import (CreateResortBooking, AdminListBookings, GetBookingSummary, CreateAdventureBooking, GetAdventureBooking,
                    ListAdventureBookings, StaffListBookings, StaffAdventureBookings, ChangeResortBookingStatus,
                    StaffResortBookingFilter, StaffSearchResortBooking, RecentResortBookings, RecentActivityBookings,
                    AddResortReview, ListResortReviews, AddAdventureReview, ListAdventureReviews, AddDestinationReview, ListDestinationReviews,
                    UserResortBookings,UserAdventureBookings, ListCoupons,UserListCoupons, AddCoupon, DeleteCoupon, GetResortPayment,
                    DeleteResortReview, CheckResortAvailability, CancelResortBooking, GetReviewImages)

from . import views


urlpatterns = [
    path('checkresortavailability/<date>', CheckResortAvailability.as_view()),
    path('cancelresortbooking/<int:booking_id>', CancelResortBooking.as_view()),
    path('createbookingresort/', CreateResortBooking.as_view()),
    path('admingetallbookings/', AdminListBookings.as_view()),
    path('getbookingsummary/<int:booking_id>', GetBookingSummary.as_view()),
    path('getpaymentsummery/<int:booking_id>', GetResortPayment.as_view()),

    path('createbookingadventure/', CreateAdventureBooking.as_view()),
    path('adventurebookingsummary/<int:booking_id>', GetAdventureBooking.as_view()),
    path('admingetadventurebookings/', ListAdventureBookings.as_view()),

    path('stafflistresortbookings/<int:user_id>', StaffListBookings.as_view()),
    path('stafflistadventurebookings/<int:user_id>', StaffAdventureBookings.as_view()),
    path('changebookingstatus/<int:value>/<int:booking_id>', ChangeResortBookingStatus.as_view()),

    path('userresortbookings/<int:user_id>', UserResortBookings.as_view()),
    path('useractivitybookings/<int:user_id>', UserAdventureBookings.as_view()),

    path('filterresortbooking/<int:user_id>/<int:value>', StaffResortBookingFilter.as_view()),
    path('searchresortbooking/<int:user_id>', StaffSearchResortBooking.as_view()),

    path('recentresortbookings/', RecentResortBookings.as_view()),
    path('recentactivitybookings/', RecentActivityBookings.as_view()),


    path('addresortreview/', AddResortReview.as_view()),
    path('addadventurereview/', AddAdventureReview.as_view()),
    path('adddestinationreview/', AddDestinationReview.as_view()),
    path('getresortreview/<int:resort_id>', ListResortReviews.as_view()),
    path('getadventurereview/<int:resort_id>', ListAdventureReviews.as_view()),
    path('getdestinationreview/<int:resort_id>', ListDestinationReviews.as_view()),

    path('deleteresortreview/<int:review_id>', DeleteResortReview.as_view()),

    path('adminlistcoupons/', ListCoupons.as_view()),
    path('userlistcoupons/<int:user_id>', UserListCoupons.as_view()),
    path('adminaddcoupon/', AddCoupon.as_view()),
    path('admindeletecoupon/<int:c_id>', DeleteCoupon.as_view()),

    path('pay/', views.start_payment, name='start_payment'),
    path('payment/success/', views.handle_payment_success, name='handle_payment_success'),
    path('activitypay/', views.activity_pay, name='start_activitypayment'),
    path('activitypayment/success/', views.activity_payment_success, name='activity_payment_success'),

    path('getreviewimages/', GetReviewImages.as_view()),
]
