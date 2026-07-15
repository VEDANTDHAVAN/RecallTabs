# Capture Pipeline

The current `POST /api/v1/tabs/capture` path calls `TabCaptureService.capture` synchronously.

```text
extension extraction
  -> URL ignore/searchable decision
  -> persist Tab
  -> word chunking + one embedding request per chunk
  -> semantic similar-tab relationships
  -> LLM summary/keywords/topic/category
  -> topic create/select
  -> tab importance update
  -> LLM entity extraction + entity/tab links
  -> LLM relationship extraction + entity relationships
  -> session assignment -> cluster assignment
```

It exits early for ignored URLs or empty content. Every repository write commits independently; a later model/provider failure leaves partial persisted state. The extension retries failed HTTP uploads, but the API has no job record, idempotency key, server retry, progress event, or compensation mechanism.

Observed implementation defects: `SessionDetectionService` and `TimelineService` read `tab.topic`, while the current model has `topic_id` and `topic_ref`; the session vector repository expects a missing session embedding field. These must be resolved before pipeline extraction.

The approved direction is not to replace this service wholesale. First characterize the capture endpoint with tests, then extract validation and persist semantics, followed by independently testable enrichment steps behind the same orchestration method.
