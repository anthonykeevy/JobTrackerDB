# EPC-15.3: Cost Tracking & Usage Auditing

**Epic:** Epic 15 - API Key & Cost Management  
**Story Owner:** Backend Developer  
**Priority:** High  
**Estimated Effort:** 10 hours  
**Status:** Draft  

## User Story

As a user or administrator,  
I want detailed cost tracking and usage auditing for AI services,  
So that I can monitor expenses, optimize usage, and maintain transparency about AI service costs.

## Background

The platform needs comprehensive cost tracking for AI service usage to provide transparency to users and enable cost optimization. This includes token-level tracking, real-time cost calculation, historical pricing, and detailed usage analytics. The system must track costs per user, per key, per model, and per conversation type to enable granular cost analysis and optimization.

## Acceptance Criteria

1. **Token Usage Tracking**
   - [ ] Track prompt, completion, and total tokens for each request
   - [ ] Log token usage with timestamp and user context
   - [ ] Calculate costs using real-time provider rates
   - [ ] Store historical pricing data for accurate cost backtracking

2. **Cost Calculation**
   - [ ] Real-time cost calculation based on current provider rates
   - [ ] Support for different pricing models (per-token, per-request)
   - [ ] Currency conversion for international users
   - [ ] Tax calculation for Australia (GST)

3. **Usage Analytics**
   - [ ] Cost breakdown by user, company, and app scope
   - [ ] Usage patterns by model and conversation type
   - [ ] Cost trends over time
   - [ ] Anomaly detection for unusual usage patterns

4. **User Dashboards**
   - [ ] Personal usage dashboard for individual users
   - [ ] Company-wide usage dashboard for administrators
   - [ ] Cost projections and budgeting tools
   - [ ] Usage alerts and notifications

5. **Audit Trail**
   - [ ] Complete audit trail for all AI service usage
   - [ ] Detailed logs for cost calculations
   - [ ] Historical pricing data retention
   - [ ] Compliance reporting capabilities

## Technical Requirements

### Database Schema
```sql
CREATE TABLE AIUsage (
    UsageID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    APIKeyID INT NOT NULL,
    Provider NVARCHAR(50) NOT NULL, -- 'OpenAI', 'Anthropic', etc.
    Model NVARCHAR(100) NOT NULL,
    ConversationType NVARCHAR(50) NOT NULL, -- 'resume_generation', 'job_matching', etc.
    PromptTokens INT NOT NULL,
    CompletionTokens INT NOT NULL,
    TotalTokens INT NOT NULL,
    CostUSD DECIMAL(10,4) NOT NULL,
    CostAUD DECIMAL(10,4) NOT NULL,
    ExchangeRate DECIMAL(10,6),
    RequestTimestamp DATETIME2 NOT NULL,
    ProcessingTimeMS INT,
    Success BIT NOT NULL,
    ErrorMessage NVARCHAR(MAX),
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (APIKeyID) REFERENCES APIKeys(APIKeyID)
);

CREATE TABLE ModelPricing (
    PricingID INT PRIMARY KEY IDENTITY(1,1),
    Provider NVARCHAR(50) NOT NULL,
    Model NVARCHAR(100) NOT NULL,
    InputPricePer1K DECIMAL(10,6) NOT NULL, -- USD per 1K tokens
    OutputPricePer1K DECIMAL(10,6) NOT NULL, -- USD per 1K tokens
    EffectiveDate DATETIME2 NOT NULL,
    EndDate DATETIME2,
    IsActive BIT DEFAULT 1,
    CreatedAt DATETIME2 DEFAULT GETDATE()
);

CREATE TABLE CostAllocation (
    AllocationID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT,
    CompanyID INT,
    PeriodStart DATETIME2 NOT NULL,
    PeriodEnd DATETIME2 NOT NULL,
    TotalCostUSD DECIMAL(10,2) NOT NULL,
    TotalCostAUD DECIMAL(10,2) NOT NULL,
    TokenCount INT NOT NULL,
    RequestCount INT NOT NULL,
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
);
```

### Cost Calculation Service
```python
class CostCalculationService:
    def calculate_cost(self, provider: str, model: str, prompt_tokens: int, 
                      completion_tokens: int) -> CostBreakdown:
        # Get current pricing for model
        # Calculate input and output costs
        # Apply exchange rate for AUD
        # Add tax calculations
        pass
    
    def get_usage_summary(self, user_id: int, start_date: datetime, 
                         end_date: datetime) -> UsageSummary:
        # Aggregate usage data for period
        # Calculate costs by model and type
        # Generate trends and insights
        pass
```

### API Endpoints
- `GET /api/usage/summary/{userId}` - Get usage summary for user
- `GET /api/usage/detailed/{userId}` - Get detailed usage logs
- `GET /api/usage/company/{companyId}` - Get company usage summary
- `GET /api/costs/projection/{userId}` - Get cost projections
- `POST /api/usage/export/{userId}` - Export usage data
- `GET /api/pricing/models` - Get current model pricing

### Analytics Dashboard
- Real-time usage monitoring
- Cost breakdown by model and type
- Usage trends and patterns
- Budget alerts and notifications
- Export capabilities for reporting

## Dev Notes

### Implementation Approach
1. Create database schema for usage tracking
2. Implement cost calculation service
3. Add usage logging to AI service calls
4. Create analytics dashboard
5. Implement reporting and export features
6. Add monitoring and alerting

### Key Dependencies
- EPC-15.1 and EPC-15.2 (API Key Management)
- AI service integration layer
- Currency exchange rate service
- Tax calculation service
- Dashboard and reporting system

### Testing Strategy
- Unit tests for cost calculations
- Integration tests for usage tracking
- Performance tests for analytics queries
- Data accuracy validation tests

### Performance Considerations
- Optimize database queries for analytics
- Implement caching for pricing data
- Use materialized views for complex aggregations
- Batch processing for large datasets

## Definition of Done

- [ ] Token usage tracking works correctly
- [ ] Cost calculations are accurate and real-time
- [ ] Usage analytics dashboard is functional
- [ ] Audit trail captures all usage data
- [ ] Export and reporting features work
- [ ] Performance meets requirements
- [ ] Error handling is comprehensive
- [ ] Documentation is complete
- [ ] Code review is approved
- [ ] Tests pass with >90% coverage

## File List

- `backend/services/cost_calculation_service.py` - Cost calculation logic
- `backend/services/usage_tracking_service.py` - Usage tracking
- `backend/models/ai_usage.py` - Usage data models
- `backend/api/usage.py` - Usage analytics endpoints
- `backend/database/migrations/003_create_usage_tracking.sql` - Database schema
- `backend/tests/test_cost_calculation.py` - Cost calculation tests
- `frontend/components/UsageDashboard.tsx` - Usage dashboard
- `frontend/components/CostAnalytics.tsx` - Cost analytics
- `docs/analytics/usage-tracking.md` - Analytics documentation 