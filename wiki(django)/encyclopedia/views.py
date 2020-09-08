from django.shortcuts import render
from django.http import HttpResponseRedirect
from markdown import markdown
import html2markdown
import random
import math

from . import util

def index(request):
    if request.method == 'POST':
        query = request.POST['q'].lower()
        entries = util.list_entries()
        search_results = []
        for entry in entries:
            entry_low = entry.lower()
            if entry_low == query:
                return HttpResponseRedirect(entry)
            if query in entry_low:
                search_results.append(entry)
        return render(request, "encyclopedia/search-results.html", {
            "search_results": search_results,
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(title)
    else:
        return render(request, "encyclopedia/create.html", {
            "title": request.GET['title'] if request.GET else "",
            "content": request.GET['content'] if request.GET else "",
        })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry_html": markdown(util.get_entry(title)),
        "entry_md": util.get_entry(title)
    })

def random_entry(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(random_entry)