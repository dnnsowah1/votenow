from django.shortcuts import render, redirect
from .models import Portfolio, Candidate, Voter

def login(request):
    if request.method == 'POST':
        password = request.POST['password']
        try:
            voter = Voter.objects.get(password=password)
            if voter.has_voted:
                return render(request, 'voting/login.html', {'error': 'You have already voted.'})
            request.session['voter_id'] = voter.id
            return redirect('vote')
        except Voter.DoesNotExist:
            return render(request, 'voting/login.html', {'error': 'Invalid password'})
    return render(request, 'voting/login.html')

def vote(request):
    if 'voter_id' not in request.session:
        return redirect('login')
    
    voter = Voter.objects.get(id=request.session['voter_id'])
    if request.method == 'POST':
        for portfolio in Portfolio.objects.all():
            candidate_id = request.POST.get(str(portfolio.id))
            if candidate_id:
                candidate = Candidate.objects.get(id=candidate_id)
                candidate.votes += 1
                candidate.save()
        voter.has_voted = True
        voter.save()
        del request.session['voter_id']
        return redirect('login')

    portfolios = Portfolio.objects.all()
    portfolios_with_candidates = [
        {'portfolio': portfolio, 'candidates': Candidate.objects.filter(portfolio=portfolio)}
        for portfolio in portfolios
    ]
    return render(request, 'voting/vote.html', {'portfolios_with_candidates': portfolios_with_candidates})

def results(request):
    portfolios = Portfolio.objects.all()
    candidates = {portfolio: Candidate.objects.filter(portfolio=portfolio).order_by('-votes') for portfolio in portfolios}
    return render(request, 'voting/results.html', {'portfolios': portfolios, 'candidates': candidates})
