# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
import datetime
from pytz import timezone

from createbox.models import Box
import logging
#dxf stuff
import DXF.drawMaze
import DXF.make_id
import DXF.make_pieces
import DXF.joinDXF
import RSS

def index(request):
    latest_box_list = Box.objects.all().order_by('-pub_date')
    for box in latest_box_list:
        box.htmlMaze
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

    latest_news = RSS.getLatestNews()
    return render_to_response('index.html', { 'boxes': boxes, 'news': latest_news })

def details(request, id):
    try:
        box = Box.objects.get(pk=id)
    except Box.DoesNotExist:
        logging.warn( "no such box id %s" % id )
        raise Http404
    
    try:
        thickness = request.POST['thickness']
    except:
        return render_to_response('detail.html', {'box': box, 'maze': box.htmlMaze(), 'version' : settings.DXFVERSION }, context_instance=RequestContext(request))

    #validate thickness
    try:
        float(thickness)
    except ValueError:
        err_msg = "'%s' isn't a number" % thickness
        logging.warn(err_msg)
        return render_to_response('detail.html', { 'box':box, 'error_message': err_msg, 'maze': box.htmlMaze(), 'version' : settings.DXFVERSION }, context_instance=RequestContext(request))
    if float(thickness) > 8 or float(thickness) < 3:
        err_msg = "thickness needs to be between 3 and 8mm"
        logging.warn(err_msg)
        return render_to_response('detail.html', { 'box':box, 'error_message': err_msg, 'maze': box.htmlMaze(), 'version' : settings.DXFVERSION }, context_instance=RequestContext(request))

    #make the DXF
    #TODO better error handling
    try:
        DXF.drawMaze.drawMaze( box.maze,box )
        DXF.make_pieces.make_pieces(float(thickness))
        DXF.make_id.make_id(box.id)
        DXF.joinDXF.joinDXF(box.id)
    except Exception as e:
        err_msg = "error making DXF: ", e.args
        logging.error(err_msg)
        return render_to_response('detail.html', { 'box':box, 'error_message': err_msg, 'maze': box.htmlMaze(), 'version' : settings.DXFVERSION }, context_instance=RequestContext(request))

    link = "/boxes/boxmaze_%i.dxf" % box.id
    return render_to_response('detail.html', {'box': box, 'plans' : link, 'thickness' : thickness, 'maze': box.htmlMaze(), 'version' : settings.DXFVERSION },
        context_instance=RequestContext(request))
    

def create(request ):
    try:
        mazeJSON = request.POST['mazejson']
    except:
        return render_to_response('create.html',
            context_instance=RequestContext(request))

    box = Box(pub_date=datetime.datetime.now(timezone('GMT')),maze=mazeJSON,version=settings.DXFVERSION)
    box.clean()
    box.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('createbox.views.details', args=(box.id,)))
