def user_listing_path(instance, filename):
    return 'user_{}/listings/{}'.format(instance.seller.user.id, filename)