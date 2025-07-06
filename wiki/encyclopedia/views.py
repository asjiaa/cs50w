import random

from markdown2 import Markdown

from django.shortcuts import render, redirect

from . import forms
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    markdowner = Markdown()
    content = util.get_entry(entry)
    if content == None:
        return render (
            request, "encyclopedia/error.html", {
                "entry": entry,
            })
    
    return render(
        request, "encyclopedia/entry.html", {
            "entry": entry,
            "content": markdowner.convert(content)
        })


def search(request):
    if request.method == "GET":
        query = request.GET.get("q")
        if query:
            entries = util.list_entries()
            results = []
            for entry in entries:
                if query.lower().strip() == entry.lower().strip():
                    return redirect("entry", entry=entry)
                
                if query.lower().strip() in entry.lower().strip():
                    results.append(entry)

            if not results:
                return render(request, "encyclopedia/search.html", {
                    "query": query,
                    "results": results,
                })
            
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "results": results
            })
        
    return render(request, "encyclopedia/search.html", {
        "results": util.list_entries()
    })


def create(request):
    if request.method == "POST":
        form = forms.CreateForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data
            error = util.get_entry(entry["title"])
            if not error:
                util.save_entry(entry["title"], entry["content"])
                return redirect("entry", entry=entry["title"])
            
            return render(request, "encyclopedia/create.html", {
                "form": form,
                "error": error,
                "entry": entry["title"]
            })

        return render(request, "encyclopedia/create.html", {
            "form": form
        })
    
    return render(request, "encyclopedia/create.html", {
        "form": forms.CreateForm()
    })


def edit(request, entry):
    content = {"content": util.get_entry(entry)}
    if request.method == "POST":
        form = forms.EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(entry, content)
            return redirect("entry", entry=entry)
        
        return render(request, "encyclopedia/edit.html", {
            "entry": entry,
            "form": forms.EditForm(initial=content),
        })
    
    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "form": forms.EditForm(initial=content),
    })


def random_page(request):
    entries = util.list_entries()
    entry = entries[random.randint(0, (len(entries) - 1))]
    return redirect("entry", entry=entry)
    