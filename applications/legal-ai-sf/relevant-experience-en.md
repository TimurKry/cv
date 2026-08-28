# Relevant experience — Senior Full-Stack Engineer (legal AI, San Francisco)

My generative-AI work is product-level rather than infrastructure-level, and I
would rather be precise about that than overstate it.

**Shipping LLM functionality inside a product.**
In TripTogether (github.com/TimurKry/meeting-point-finder) I built the whole path
end to end: a React/TypeScript frontend and a Node.js backend that aggregates
several external REST data sources, normalizes their inconsistent responses into
one structured shape, and passes that structured context to the Google Gemini API
to rank candidate results. The interesting engineering was not the model call. It
was everything around it - reconciling third-party schemas that disagree with each
other, handling partial and failed upstream responses, and shaping the model
output into something the UI can render reliably rather than something that
happens to look right once.

**Structured extraction from documents.**
At Straumann Group I built a management tool that parsed XML files and extracted
stock levels, product relationships and compatibility rules, then presented them
as tables the business could actually read and act on. That is the same shape of
problem as your legal fact extraction - take semi-structured documents, pull out
the entities and the relationships between them, surface them so a human can
decide - though at business-unit scale, not millions of contracts.

**Working AI-natively.**
Cursor and Claude are my daily development workflow, not an add-on. My most recent
project (github.com/TimurKry/dvizh-patrol) is a Next.js 16 / React 19 /
TypeScript / Tailwind v4 / Supabase mobile-first PWA with Playwright and Vitest
suites, built end to end that way. I have integrated the OpenAI API alongside
Gemini.

**Full stack.**
Six years commercial: TypeScript, React, Next.js, Node.js, Postgres and MySQL,
REST and XML integration. Three of those years at Straumann Group, where I
modernized an internal B2B ordering platform - UI and UX rebuilt, legacy code
migrated, new validation logic added, while the underlying ordering logic stayed
intact. Before that, seven freelance projects delivered alone from requirements
to launch.

**To be straight with you:** I have not built RAG systems, agentic orchestration,
or pipelines processing documents at the millions scale. What I bring is
end-to-end product delivery, real LLM integration in shipped code, comfort inside
legacy systems I did not write, and a strong bias toward having something working
today rather than designed tomorrow.
