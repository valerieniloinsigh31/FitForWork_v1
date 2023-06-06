from django import template


register = template.Library() #variable called register, instance of template.Library()...creating custom template tags-django docs

@register.filter(name='calc_subtotal') #decorator
def calc_subtotal(price, quantity): #function that takes in price and quantity as parameters and returns their product
    return price * quantity