# Epic 15: API Key & Cost Management

**Epic Owner:** Architect / DevOps

**Goal:** Securely manage application and user-provided API keys for AI services, support model flexibility and provider abstraction, and ensure detailed cost tracking and regulatory compliance.

**Background:**
As part of enabling LLM capabilities for AI-driven features (e.g., resume tailoring, job matching), the platform must support internal and user-supplied API keys for model access. Users may opt to provide their own API keys to use specific models or manage costs. The system must securely store and manage these keys, enable tiered model selection per use case, and log all usage with token-level granularity for cost auditing and transparency. Security compliance with GDPR, SOC2, and Australian data laws is mandatory.

**Key Features:**

1. **Secure Key Storage and Encryption**
   * Encrypt keys using app-encrypted blob via Azure Key Vault
   * Backend-only access to decrypt and use keys
   * Comply with GDPR and SOC2 audit trails
   * AES-256 encryption for all stored API keys
   * No plaintext key retrieval after submission (replace/delete only)

2. **Multi-Scope API Key Hierarchy**
   * User key overrides company and app
   * Company key applies to all users in org unless overridden
   * Admin console for managing company/app keys
   * Role-based access control: Only Admin users can manage API keys for App/Company/User scope
   * Key fallback logic: User > Company > App

3. **Model Routing and Flexibility**
   * Allow keys to specify default model (e.g. GPT-4, Claude)
   * Enable prompt-type to model mapping for optimization
   * Abstract AI providers via pluggable backend architecture
   * Support for prompt-type based model routing
   * API key record includes: encrypted key, scope (App, Company, User), provider, preferred model, metadata, and validity periods

4. **Cost Logging and Usage Auditing**
   * Token usage logging (prompt, completion, total tokens)
   * USD cost per request calculated via real-time provider rates
   * Usage records include: model, key ID (scope), conversation type, timestamps
   * Retain historical price matrix per model for accurate cost backtracking
   * Maintain historical cost integrity with model pricing per period (start and end date)

5. **User and Company Dashboards**
   * Token and cost usage summaries per user, per key
   * Visibility into active key scope (used/fallback)
   * Cost budget warnings and limits (future feature)
   * Users can input and rotate their own API keys securely via frontend

6. **Compliance and Monitoring**
   * Role-based UI and access to key management
   * Admin audit logs for key creation, update, deletion
   * Support key rotation with expiry tracking
   * Regional storage (Azure AU) and provider-locality awareness
   * Security compliance with GDPR, SOC2, and Australian data laws

**Success Metrics:**
* % of users with own keys onboarded
* Error-free model routing accuracy
* Token cost savings per model optimization
* Compliance audit readiness score (SOC2/GDPR checks)
* API key security incident rate
* Cost tracking accuracy and transparency

**Dependencies:**
* Azure Key Vault
* FastAPI security and role-based access
* AI Provider SDKs (OpenAI, Anthropic, etc.)
* Usage logging and reporting service
* Core infrastructure (Epic 8)
* Authentication system (Epic 7)
* AI service integration (Epic 14)

**Acceptance Criteria:**
* Users and companies can securely input, update, and delete API keys
* Keys are encrypted and only decrypted at runtime on backend
* Key hierarchy (User > Company > App) applies to all AI prompts
* Each prompt logged with tokens and cost against correct key
* Model switching supported per prompt type and key
* Dashboards show usage metrics with correct attribution and cost breakdown
* Compliance requirements are met for data storage and access
* Key rotation and expiry management works correctly
* Cost tracking is accurate and transparent to users

**Priority:** High

**Tags:** api-key-management, cost-tracking, ai-usage, encryption, azure-key-vault, compliance, provider-abstraction, model-routing, role-based-access, security, audit-trail 