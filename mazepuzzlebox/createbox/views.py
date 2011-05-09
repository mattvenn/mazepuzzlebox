# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
import datetime
from pytz import timezone

from createbox.models import Box
from createbox.drawMaze import drawMaze, checkJSON
import logging

def index(request):
    latest_box_list = Box.objects.all().order_by('-pub_date')[:5]
    return render_to_response('index.html', { 'latest_box_list': latest_box_list, })

def details(request, id):
    try:
        box = Box.objects.get(pk=id)
    except Box.DoesNotExist:
        logging.warn( "no such box id %s" % id )
        raise Http404
    
    try:
        thickness = request.POST['thickness']
    except:
        return render_to_response('detail.html', {'box': box}, context_instance=RequestContext(request))

    #validate thickness
    try:
        float(thickness)
    except ValueError:
        err_msg = "'%s' isn't a number" % thickness
        logging.warn(err_msg)
        return render_to_response('detail.html', { 'box':box, 'error_message': err_msg, }, context_instance=RequestContext(request))
    if float(thickness) > 8 or float(thickness) < 3:
        err_msg = "thickness needs to be between 3 and 8mm"
        logging.warn(err_msg)
        return render_to_response('detail.html', { 'box':box, 'error_message': err_msg, }, context_instance=RequestContext(request))

    #generate the DXF
    from subprocess import call
    buildcommand = settings.ROOT_DIR + "DXF/buildall.sh"
    logging.debug( "building DXF" )
    retcode = call([buildcommand,str(box.id),thickness,box.maze])
    if retcode != 0:
        logging.debug( "got return code %i" % retcode )
        err_msg = "problem with rendering DXF for id %s thickness %s maze %s" % ( box.id, thickness, box.maze )
        logging.error(err_msg)
        return render_to_response('detail.html', { 'box':box, 'error_message': err_msg, }, context_instance=RequestContext(request))

    link = "/boxes/boxmaze_%i.dxf" % box.id
    return render_to_response('detail.html', {'box': box, 'plans' : link, 'thickness' : thickness },
        context_instance=RequestContext(request))
    

def create(request ):
    try:
        mazeJSON = request.POST['maze']
    except:
        return render_to_response('create.html',
            context_instance=RequestContext(request))

    #error check json string
    try:
        checkJSON(mazeJSON)
    except Exception as e:
        err_msg = "bad json: %s" % e
        logging.warn(err_msg)
        return render_to_response('create.html', { 'error_message': err_msg },
            context_instance=RequestContext(request))

    box = Box(pub_date=datetime.datetime.now(timezone('GMT')),maze=mazeJSON)
    box.save()
    #make the maze png, gets saved to a file
    drawMaze(mazeJSON,box.id)
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('createbox.views.details', args=(box.id,)))
