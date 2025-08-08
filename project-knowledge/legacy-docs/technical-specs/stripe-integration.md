# Stripe Integration Technical Specification

## Overview

This document outlines the technical implementation of Stripe integration for the AI-Powered Resume and Job Tracker Platform's billing and payment system.

## Architecture

### Components
1. **Stripe API Integration** - Backend service for Stripe operations
2. **Webhook Handler** - Processes Stripe webhook events
3. **Billing Service** - Manages subscription and billing logic
4. **Database Schema** - Stores billing and subscription data
5. **Frontend Components** - User billing interface

### Data Flow
```
User → Frontend → Backend → Stripe API
Stripe → Webhook → Backend → Database
```

## Database Schema

### Core Tables

#### `Subscriptions`
```sql
CREATE TABLE Subscriptions (
    SubscriptionID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    StripeSubscriptionID NVARCHAR(255) NOT NULL,
    Status NVARCHAR(50) NOT NULL, -- active, past_due, canceled, etc.
    CurrentPeriodStart DATETIME2 NOT NULL,
    CurrentPeriodEnd DATETIME2 NOT NULL,
    CancelAtPeriodEnd BIT DEFAULT 0,
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    UpdatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
```

#### `PaymentMethods`
```sql
CREATE TABLE PaymentMethods (
    PaymentMethodID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    StripePaymentMethodID NVARCHAR(255) NOT NULL,
    Type NVARCHAR(50) NOT NULL, -- card, bank_account, etc.
    Last4 NVARCHAR(4),
    Brand NVARCHAR(50), -- visa, mastercard, etc.
    ExpMonth INT,
    ExpYear INT,
    IsDefault BIT DEFAULT 0,
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
```

#### `Invoices`
```sql
CREATE TABLE Invoices (
    InvoiceID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    StripeInvoiceID NVARCHAR(255) NOT NULL,
    SubscriptionID INT,
    Amount INT NOT NULL, -- Amount in cents
    Currency NVARCHAR(3) DEFAULT 'AUD',
    Status NVARCHAR(50) NOT NULL, -- draft, open, paid, void, etc.
    DueDate DATETIME2,
    PaidAt DATETIME2,
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (SubscriptionID) REFERENCES Subscriptions(SubscriptionID)
);
```

#### `BillingEvents`
```sql
CREATE TABLE BillingEvents (
    EventID INT PRIMARY KEY IDENTITY(1,1),
    StripeEventID NVARCHAR(255) NOT NULL,
    EventType NVARCHAR(100) NOT NULL,
    UserID INT,
    SubscriptionID INT,
    InvoiceID INT,
    EventData NVARCHAR(MAX), -- JSON payload
    ProcessedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (SubscriptionID) REFERENCES Subscriptions(SubscriptionID),
    FOREIGN KEY (InvoiceID) REFERENCES Invoices(InvoiceID)
);
```

## API Endpoints

### Subscription Management

#### `POST /api/billing/subscriptions`
Create a new subscription
```json
{
  "paymentMethodId": "pm_1234567890",
  "planId": "price_monthly_10"
}
```

#### `GET /api/billing/subscriptions/{subscriptionId}`
Get subscription details

#### `PUT /api/billing/subscriptions/{subscriptionId}`
Update subscription (upgrade/downgrade)

#### `DELETE /api/billing/subscriptions/{subscriptionId}`
Cancel subscription

### Payment Methods

#### `POST /api/billing/payment-methods`
Add a new payment method
```json
{
  "type": "card",
  "card": {
    "number": "4242424242424242",
    "exp_month": 12,
    "exp_year": 2025,
    "cvc": "123"
  }
}
```

#### `GET /api/billing/payment-methods`
List user's payment methods

#### `PUT /api/billing/payment-methods/{paymentMethodId}`
Update payment method

#### `DELETE /api/billing/payment-methods/{paymentMethodId}`
Remove payment method

### Invoices

#### `GET /api/billing/invoices`
List user's invoices

#### `GET /api/billing/invoices/{invoiceId}`
Get invoice details

#### `GET /api/billing/invoices/{invoiceId}/download`
Download invoice PDF

## Webhook Events

### Required Events
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.payment_succeeded`
- `invoice.payment_failed`
- `payment_method.attached`
- `payment_method.detached`
- `charge.dispute.created`

### Webhook Handler Implementation
```python
@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400)
    
    # Handle the event
    if event['type'] == 'customer.subscription.created':
        handle_subscription_created(event)
    elif event['type'] == 'invoice.payment_succeeded':
        handle_payment_succeeded(event)
    # ... handle other events
    
    return {"status": "success"}
```

## Security Considerations

### PCI Compliance
- Never store full credit card numbers
- Use Stripe Elements for secure card collection
- Implement proper webhook signature verification
- Use HTTPS for all payment-related communications

### Data Protection
- Encrypt sensitive billing data at rest
- Implement proper access controls for billing data
- Audit log all billing operations
- Regular security assessments

### Error Handling
- Graceful handling of Stripe API failures
- Retry logic for failed webhook processing
- Data consistency between Stripe and local database
- Comprehensive error logging and monitoring

## Environment Configuration

### Development
```python
STRIPE_PUBLISHABLE_KEY = "pk_test_..."
STRIPE_SECRET_KEY = "sk_test_..."
STRIPE_WEBHOOK_SECRET = "whsec_test_..."
```

### Production
```python
STRIPE_PUBLISHABLE_KEY = "pk_live_..."
STRIPE_SECRET_KEY = "sk_live_..."
STRIPE_WEBHOOK_SECRET = "whsec_live_..."
```

## Testing Strategy

### Unit Tests
- Mock Stripe API responses
- Test webhook signature verification
- Validate subscription state transitions
- Test payment method validation

### Integration Tests
- Test complete subscription flow
- Verify webhook processing
- Test payment failure scenarios
- Validate invoice generation

### End-to-End Tests
- Complete user subscription journey
- Payment method management
- Subscription cancellation flow
- Admin billing operations

## Monitoring & Analytics

### Key Metrics
- Payment success rate
- Subscription churn rate
- Webhook processing success rate
- API response times
- Error rates by operation type

### Alerts
- Payment failure rate > 5%
- Webhook processing failures
- Stripe API errors
- Subscription creation failures

## Implementation Phases

### Phase 1: Core Integration
1. Stripe API setup and configuration
2. Basic subscription creation
3. Webhook handler implementation
4. Database schema creation

### Phase 2: Payment Management
1. Payment method management
2. Invoice generation and delivery
3. Payment failure handling
4. User billing interface

### Phase 3: Advanced Features
1. Subscription upgrades/downgrades
2. Prorated billing
3. Refund processing
4. Admin billing dashboard

### Phase 4: Optimization
1. Performance optimization
2. Advanced analytics
3. Multi-currency support
4. Tax calculation automation

## Dependencies

### External Services
- Stripe API
- Email service (for invoice delivery)
- PDF generation service (for invoices)

### Internal Dependencies
- User authentication system
- Database migration system
- Logging and monitoring
- Admin dashboard

## Cost Considerations

### Stripe Fees
- 1.75% + 30¢ per successful card charge (Australia)
- No monthly fees
- Additional fees for international cards

### Infrastructure Costs
- Database storage for billing data
- Webhook processing compute
- PDF generation for invoices
- Email delivery for receipts

## Compliance Requirements

### Australia-Specific
- GST calculation and reporting
- ABN validation for business customers
- Tax invoice requirements
- Consumer protection compliance

### General
- PCI DSS compliance
- Data protection regulations
- Financial reporting requirements
- Audit trail maintenance 