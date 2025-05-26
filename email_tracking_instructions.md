# Email Tracking Template Instructions

## Purpose
This comprehensive email tracking system helps organize all email evidence for your case.

## Column Descriptions

### Identification Fields
- **email_id**: Unique identifier (e.g., EM-001, EM-002)
- **thread_id**: Groups related emails in a conversation
- **in_reply_to**: ID of email this responds to

### Temporal Fields
- **date_sent/time_sent**: When email was sent
- **date_received/time_received**: When received (from headers)
- **days_to_response**: Business days until response (if any)

### Party Information
- **from/to/cc/bcc**: Names, emails, and titles
- **mentioned_parties**: Anyone referenced in the email

### Content Classification
- **category**: Main type (accommodation_request, denial, retaliation, etc.)
- **subcategory**: Specific subtype
- **keywords**: Searchable terms

### Legal Analysis
- **legal_significance**: Why this email matters
- **violation_type**: Specific legal violations evidenced
- **damage_relevance**: How it supports damages

### Discovery & Evidence
- **exhibit_number**: Formal exhibit designation
- **roi_reference**: Where found in investigation
- **production_bates**: Discovery production numbers

### Technical/Preservation
- **metadata_preserved**: Yes/No
- **hash_value**: For authentication
- **file_path**: Where stored

### Review Tracking
- **review_status**: Not Started/In Progress/Complete
- **flag_for_attorney**: Priority items
- **action_required**: Next steps

## Best Practices
1. Use consistent date format (YYYY-MM-DD)
2. Preserve email metadata
3. Track every follow-up
4. Note response times carefully
5. Cross-reference with other evidence
6. Update regularly as case progresses
