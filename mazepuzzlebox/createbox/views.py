# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
import datetime
from pytz import timezone

from createbox.models import ContactForm
from createbox.models import Box
from createbox.models import Testimonial
import logging
#dxf stuff
import DXF.drawMaze
import DXF.make_id
import DXF.make_pieces
import DXF.ezjoinDXF
import DXF.buildInstructions
import DXF.drawInstructionsMaze 
import RSS


def index(request):
    latest_box_list = Box.objects.all().order_by('-pub_date')
#    for box in latest_box_list:
#        box.htmlMaze
    paginator = Paginator(latest_box_list, 5)
    page = request.GET.get('page')
    try:
        boxes = paginator.page(page)
    except TypeError:
        boxes = paginator.page(1)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        boxes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        boxes = paginator.page(paginator.num_pages)

    #news
    latest_news = [] #RSS.getLatestNews()

    #testimonials
    testimonial = Testimonial.objects.order_by('?')[0]
    return render_to_response('index.html', { 'extHTTP' :settings.EXTHTTP, 'boxes': boxes, 'news': latest_news, 'testimonial_text': testimonial.testimonial, 'testimonial_author': testimonial.author })

def details(request, id):
    try:
        box = Box.objects.get(pk=id)
    except Box.DoesNotExist:
        logging.warn( "no such box id %s" % id )
        raise Http404
    
    try:
        thickness = request.POST['thickness']
    except:
        return render_to_response('detail.html', {'extHTTP' :settings.EXTHTTP,'box': box, 'maze': box.htmlMaze(), 'version' : settings.DXFVERSION }, context_instance=RequestContext(request))

    #validate thickness
    try:
        float(thickness)
    except ValueError:
        if len(thickness) == 0: 
            err_msg = "you didn't type a number"
        else:
            err_msg = "'%s' isn't a number" % thickness
        logging.warn(err_msg)
        return render_to_response('detail.html', {'extHTTP' :settings.EXTHTTP, 'box':box, 'error_message': err_msg, 'maze': box.htmlMaze(), 'version' : settings.DXFVERSION }, context_instance=RequestContext(request))
    if float(thickness) > 8 or float(thickness) < 3:
        err_msg = "thickness needs to be between 3 and 8mm"
        logging.warn(err_msg)
        return render_to_response('detail.html', {'extHTTP' :settings.EXTHTTP, 'box':box, 'error_message': err_msg, 'maze': box.htmlMaze(), 'version' : settings.DXFVERSION }, context_instance=RequestContext(request))

    #make the DXF
    #TODO better error handling
    try:
        DXF.drawMaze.drawMaze( box.maze,box )
        DXF.make_pieces.make_pieces(float(thickness))
        DXF.make_id.make_id(box.id)
        DXF.ezjoinDXF.joinDXF(box.id)
	#SVG
        DXF.drawInstructionsMaze.drawMaze( box.maze,box )
        DXF.buildInstructions.buildInstructions(box.id)
        err_msg = "box built at thickness" + thickness
        logging.debug(err_msg)
    except Exception as e:
        err_msg = "error making DXF: ", e.args
        logging.error(err_msg)
        return render_to_response('detail.html', {'extHTTP' :settings.EXTHTTP, 'box':box, 'error_message': err_msg, 'maze': box.htmlMaze(), 'version' : settings.DXFVERSION }, context_instance=RequestContext(request))

    link = "/boxes/boxmaze_%i.dxf" % box.id
    instructionsLink = "/boxes/instructions_%i.png" % box.id
    return render_to_response('detail.html', {'extHTTP' :settings.EXTHTTP,'box': box, 'instructions' : instructionsLink,  'plans' : link, 'thickness' : thickness, 'maze': box.htmlMaze(), 'version' : settings.DXFVERSION },
        context_instance=RequestContext(request))
    

def create(request ):
    try:
        mazeJSON = request.POST['mazejson']
    except:
        return render_to_response('create.html',{ 'extHTTP' : settings.EXTHTTP},
            context_instance=RequestContext(request))

    box = Box(pub_date=datetime.datetime.now(timezone('GMT')),maze=mazeJSON,version=settings.DXFVERSION)
    box.clean()
    box.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('createbox.views.details', args=(box.id,)))

def contactview(request):
    message = request.POST.get('message', '')
    from_email = request.POST.get('email', '')
    subject = "contact from MPB"
    if message and from_email:
        try:
            send_mail(subject, message, from_email, ['matt@mattvenn.net'])
        except BadHeaderError:
            err_msg = 'Invalid header found.'
            return render_to_response('contact.html', {'extHTTP' :settings.EXTHTTP, 'error_message': err_msg}, context_instance=RequestContext(request))
        except Exception as e:
            err_msg = 'Problem sending email: ', e
            return render_to_response('contact.html', {'extHTTP' :settings.EXTHTTP, 'error_message': err_msg}, context_instance=RequestContext(request))
        return HttpResponseRedirect('/contact/thankyou')
    else:
        return render_to_response('contact.html', {'extHTTP': settings.EXTHTTP}, context_instance=RequestContext(request))

