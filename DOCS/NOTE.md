# Senior-Level Perspectives


## High Level Design 

**How to ensure the latency is below 200ms ?**
- Database (First 50ms): You’ve already solved this with UUIDv7, GIN indexes, and denormalization.
- Application Logic (Next 30ms): By pre-rendering Markdown to HTML on save, you keep this slice tiny.
- Template Rendering (Next 20ms): Django's template engine is fast, but for viral posts, use Fragment Caching.
- Example: {% cache 600 post_content post.id %}{{ post.content_html }}{% endcache %}. This stores the HTML in Redis for 10 minutes.

## Low Level Design 

Approaching the LLD with the thinking of how can I isolate this code so that when I have to delete or change it later, it doesn't break everything else. 

SOLID Principles:
- Single Responsiblity Principle:
- Open/Closed Principle: 
- Liskov Substitution Principle:
- Interface Segregation Principle:
- Dependency Inversion Principle: 


