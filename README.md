# MerchantScore — AI Credit Intelligence for Indian MSMEs

> India has 63 million MSMEs. Less than 15% have access to formal credit.
> Banks don't understand merchant businesses. MerchantScore changes that.

## What it does

MerchantScore analyzes a merchant's Razorpay transaction data across 
15 financial signals and generates:

- Real-time credit score (300-900)
- Full explainability — why is your score what it is
- 6-month trajectory — where your score is headed
- Working capital recommendation — exactly what you qualify for
- Hinglish explanation — so every merchant understands

## The Problem

A restaurant owner in Jaipur processes ₹3 lakh/month through Razorpay.
Her transaction data shows consistent revenue, low refund rate, 
high repeat customers. She's creditworthy.

But the bank sees: no collateral, no salary slip, no credit history.
Loan rejected.

MerchantScore reads what the bank can't.

## Tech Stack

- Python, XGBoost, SHAP
- FastAPI backend
- React frontend  
- Razorpay Test APIs

## Dataset

1000 synthetic merchants across 15 categories and 10 Indian cities.
15 financial signals engineered from transaction patterns.

## Credit Signals

1. Revenue consistency score
2. Monthly revenue growth rate
3. Refund rate
4. Chargeback rate
5. Customer repeat rate
6. Payment method diversity
7. Failed payment rate
8. Settlement velocity
9. Dispute resolution rate
10. Late settlement frequency
11. Revenue concentration risk
12. Average transaction value
13. Monthly transaction volume
14. Peak season ratio
15. Years active on platform

## Status

- [x] Dataset generated (1000 merchants)
- [ ] ML model training
- [ ] SHAP explainability
- [ ] FastAPI backend
- [ ] React dashboard
- [ ] Hinglish LLM explanation
- [ ] Demo video