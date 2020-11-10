from django.shortcuts import render, redirect


def app(request, route=""):
    if request.method == "GET":
        showcase = request.GET.get("showcase", False)
    else:
        showcase = False

    if request.user.is_authenticated or showcase:
        return render(request, "frontend/index.html")
    else:
        return redirect('login')