from django import template
from pitch import models as Mod
from django.core.urlresolvers import reverse, reverse_lazy
from pitch.views import getRating


register = template.Library()

@register.inclusion_tag('pitch/showpitch.html',takes_context=True)
def show_user_pitch(context, pitch):
	votes = pitch.data_set.get().votes
	color = "text-"+getRating(pitch)

	display_pitch_url = reverse('display_pitch', args=(pitch.id,))

	return {'display_pitch_url':display_pitch_url,'votes':votes, 'color':color, 'pitch':pitch}

@register.inclusion_tag('pitch/displayprocess.html',takes_context=True)
def link_profile(context, renderuser, currentuser):
	# profile_url = reverse('users')+"/profile/"+user.id
	profile_url = "#"
	return {'profile_url':profile_url, 'renderuser': renderuser, 'my':context['my'], 'user':currentuser}
