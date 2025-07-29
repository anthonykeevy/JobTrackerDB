# EPC-16.1: Stripe Integration & Setup

**Epic:** Epic 16 - Billing & Payment System  
**Story Owner:** Backend Developer  
**Priority:** High  
**Estimated Effort:** 12 hours  
**Status:** Draft  

## User Story

As a system administrator,  
I want to integrate Stripe for secure payment processing,  
So that users can subscribe to the platform and pay securely for AI-powered resume and job tracking services.

## Background

The platform operates on a $10/month subscription model with a target of 1000 subscribers by month 3. Stripe provides the necessary infrastructure for secure payment processing, subscription management, and financial reporting. This integration must handle subscription lifecycle management, payment failures, refunds, and provide clear billing transparency to users while maintaining PCI compliance.

## Acceptance Criteria

1. **Stripe API Integration**
   - [ ] Secure Stripe API integration with proper authentication
   - [ ] Environment-specific configuration (test/production)
   - [ ] Stripe SDK integration for Python/FastAPI
   - [ ] API key management and rotation procedures

2. **Webhook Handling**
   - [ ] Webhook signature verification and validation
   - [ ] Processing of all required Stripe events
   - [ ] Idempotent webhook processing
   - [ ] Comprehensive error handling and retry logic

3. **Database Schema**
   - [ ] Subscriptions table for tracking user subscriptions
   - [ ] PaymentMethods table for storing payment information
   - [ ] Invoices table for billing records
   - [ ] BillingEvents table for audit trail

4. **Security & Compliance**
   - [ ] PCI DSS compliance through Stripe
   - [ ] Secure webhook endpoint with signature verification
   - [ ] No sensitive payment data stored locally
   - [ ] Audit logging for all payment operations

5. **Error Handling**
   - [ ] Graceful handling of Stripe API failures
   - [ ] Retry logic for failed webhook processing
   - [ ] Data consistency between Stripe and local database
   - [ ] Comprehensive error logging and monitoring

## Technical Requirements

### Database Schema
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

### Stripe Service Implementation
```python
class StripeService:
    def __init__(self):
        self.stripe = stripe
        self.stripe.api_key = settings.STRIPE_SECRET_KEY
    
    async def create_subscription(self, user_id: int, payment_method_id: str) -> Subscription:
        # Create Stripe customer if not exists
        # Create subscription with payment method
        # Store subscription in local database
        pass
    
    async def handle_webhook(self, payload: bytes, signature: str) -> bool:
        # Verify webhook signature
        # Parse event and route to appropriate handler
        # Update local database
        pass
```

### Webhook Events to Handle
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.payment_succeeded`
- `invoice.payment_failed`
- `payment_method.attached`
- `payment_method.detached`
- `charge.dispute.created`

### API Endpoints
- `POST /webhooks/stripe` - Stripe webhook endpoint
- `POST /api/billing/subscriptions` - Create subscription
- `GET /api/billing/subscriptions/{subscriptionId}` - Get subscription
- `PUT /api/billing/subscriptions/{subscriptionId}` - Update subscription
- `DELETE /api/billing/subscriptions/{subscriptionId}` - Cancel subscription

## Dev Notes

### Implementation Approach
1. Set up Stripe account and configure API keys
2. Create database schema for billing data
3. Implement Stripe service with API integration
4. Create webhook handler with signature verification
5. Add comprehensive error handling and logging
6. Test with Stripe test environment

### Key Dependencies
- Stripe account and API keys
- Stripe Python SDK
- FastAPI webhook handling
- Database migration system
- User authentication system

### Testing Strategy
- Unit tests for Stripe service methods
- Integration tests with Stripe test environment
- Webhook signature verification tests
- Error handling and retry logic tests

### Security Considerations
- Never store full credit card numbers
- Use Stripe Elements for secure card collection
- Implement proper webhook signature verification
- Use HTTPS for all payment-related communications

## Definition of Done

- [ ] Stripe API integration is functional
- [ ] Webhook handling works correctly
- [ ] Database schema is implemented
- [ ] All required webhook events are processed
- [ ] Error handling is comprehensive
- [ ] Security requirements are met
- [ ] Tests pass with >90% coverage
- [ ] Documentation is complete
- [ ] Code review is approved
- [ ] PCI compliance is maintained

## File List

- `backend/services/stripe_service.py` - Stripe integration service
- `backend/services/webhook_handler.py` - Webhook processing
- `backend/models/billing.py` - Billing data models
- `backend/api/billing.py` - Billing API endpoints
- `backend/database/migrations/004_create_billing_schema.sql` - Database schema
- `backend/tests/test_stripe_integration.py` - Stripe integration tests
- `backend/tests/test_webhooks.py` - Webhook handling tests
- `docs/billing/stripe-integration.md` - Integration documentation
- `config/stripe_config.py` - Stripe configuration 