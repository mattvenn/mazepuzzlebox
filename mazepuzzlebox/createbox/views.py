# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
from pytz import timezone

from createbox.models import Box
from createbox.drawMaze import drawMaze, checkJSON

def index(request):
    latest_box_list = Box.objects.all().order_by('-pub_date')[:5]
    return render_to_response('index.html', { 'latest_box_list': latest_box_list, })

def details(request, id):
    try:
        box = Box.objects.get(pk=id)
    except Box.DoesNotExist:
        raise Http404
    
    try:
        thickness = request.POST['thickness']
    except:
        return render_to_response('detail.html', {'box': box},  
            context_instance=RequestContext(request))

    #validate thickness
    try:
        float(thickness)
    except ValueError:
        return render_to_response('detail.html', { 'box':box,
                'error_message': "'%s' isn't a number" % thickness,
            }, context_instance=RequestContext(request))
    if float(thickness) > 8 or float(thickness) < 3:
        return render_to_response('detail.html', { 'box':box,
                'error_message': "thickness needs to be between 3 and 8mm",
            }, context_instance=RequestContext(request))

    #generate the DXF
    from subprocess import call
    buildcommand = "/home/matthew/work/python/mazepuzzlebox/DXF/buildall.sh"
    call([buildcommand,str(box.id),thickness,box.maze])
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
        return render_to_response('create.html', { 'error_message': "bad json: %s" % e },
            context_instance=RequestContext(request))

    box = Box(pub_date=datetime.datetime.now(timezone('GMT')),maze=mazeJSON)
    box.save()
    #make the maze png, gets saved to a file
    drawMaze(mazeJSON,box.id)
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
#    return render_to_response('index.html', { 'latest_box_list': latest_box_list, })
    #return render_to_response('detail.html', {'box': box} )
    return HttpResponseRedirect(reverse('createbox.views.details', args=(box.id,)))
