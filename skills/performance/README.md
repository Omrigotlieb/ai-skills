# Performance Skills for Claude Code

Skills for performance optimization, profiling, and benchmarking.

---

## Performance Profiling Skill

```markdown
---
name: performance-profiling
description: Profile and identify performance bottlenecks
---

# Performance Profiling

## When to Use
- Slow application response
- High CPU/memory usage
- User-reported lag
- Before production deployment

## By Language

### JavaScript/Node.js
- Chrome DevTools Performance tab
- Node.js --inspect flag
- clinic.js (flame, doctor, bubbleprof)
- 0x (flame graphs)

### Python
- cProfile
- py-spy
- memory_profiler
- scalene

### Go
- pprof
- trace
- benchmarks

### Rust
- flamegraph
- perf
- criterion (benchmarks)

## Metrics to Track
- CPU time
- Memory allocation
- I/O wait
- Network latency
- Database query time
```

---

## Frontend Performance Skill

```markdown
---
name: frontend-performance
description: Optimize web application performance
---

# Frontend Performance

## Core Web Vitals
| Metric | Good | Description |
|--------|------|-------------|
| **LCP** | <2.5s | Largest Contentful Paint |
| **INP** | <200ms | Interaction to Next Paint |
| **CLS** | <0.1 | Cumulative Layout Shift |

## Optimization Techniques

### Bundle Size
- Tree shaking
- Code splitting
- Dynamic imports
- Analyze with webpack-bundle-analyzer

### Images
- WebP/AVIF formats
- Lazy loading
- Responsive images (srcset)
- Image CDNs

### JavaScript
- Defer non-critical scripts
- Minimize main thread work
- Web Workers for heavy computation
- Debounce/throttle events

### CSS
- Critical CSS inlining
- Remove unused styles
- Avoid @import
- CSS containment

## Tools
- Lighthouse
- WebPageTest
- Chrome DevTools
- bundlephobia
```

---

## Backend Performance Skill

```markdown
---
name: backend-performance
description: Optimize server-side performance
---

# Backend Performance

## Common Bottlenecks
1. **Database** - N+1 queries, missing indexes
2. **I/O** - Blocking calls, sync operations
3. **Memory** - Leaks, excessive allocation
4. **CPU** - Inefficient algorithms

## Optimization Strategies

### Caching
| Level | Tool | TTL |
|-------|------|-----|
| Browser | Cache headers | Hours-days |
| CDN | CloudFront, Fastly | Minutes-hours |
| Application | Redis, Memcached | Seconds-minutes |
| Database | Query cache | Varies |

### Database
- Connection pooling
- Query optimization
- Read replicas
- Indexing strategy

### Async Processing
- Message queues (Redis, RabbitMQ)
- Background jobs
- Event-driven architecture

## Monitoring
- APM tools (DataDog, New Relic)
- Custom metrics
- Distributed tracing
```

---

## Memory Optimization Skill

```markdown
---
name: memory-optimization
description: Find and fix memory issues
---

# Memory Optimization

## Memory Issues
| Type | Symptom | Fix |
|------|---------|-----|
| **Leak** | Growing memory | Find dangling refs |
| **Bloat** | High baseline | Reduce allocations |
| **Fragmentation** | Erratic behavior | Pool allocations |

## Node.js Memory
- --max-old-space-size
- heapdump
- v8.getHeapStatistics()
- process.memoryUsage()

## Techniques
- Object pooling
- Weak references
- Stream processing
- Lazy initialization

## Example: Finding Leak
1. Take heap snapshot
2. Perform suspect operation
3. Take another snapshot
4. Compare objects retained
```

---

## Algorithm Optimization Skill

```markdown
---
name: algorithm-optimization
description: Improve algorithm complexity
---

# Algorithm Optimization

## Complexity Analysis
| Big O | Name | Example |
|-------|------|---------|
| O(1) | Constant | Hash lookup |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Array scan |
| O(n log n) | Linearithmic | Merge sort |
| O(n²) | Quadratic | Nested loops |
| O(2ⁿ) | Exponential | Recursive fib |

## Common Improvements
- Replace O(n) lookup with hash map O(1)
- Use binary search instead of linear
- Memoize repeated calculations
- Use appropriate data structures

## Data Structure Selection
| Use Case | Best Structure |
|----------|----------------|
| Fast lookup | Hash map |
| Ordered data | Balanced tree |
| FIFO queue | Deque |
| Priority | Heap |
| Relationships | Graph |
```

---

## Load Testing Skill

```markdown
---
name: load-testing
description: Performance testing under load
---

# Load Testing

## Tools
| Tool | Best For |
|------|----------|
| **k6** | Developer-friendly, CI integration |
| **Artillery** | Node.js ecosystem |
| **JMeter** | Complex scenarios |
| **Locust** | Python-based |
| **wrk** | Simple HTTP benchmarks |

## Test Types
- **Smoke test** - Minimal load, verify works
- **Load test** - Expected load
- **Stress test** - Beyond capacity
- **Spike test** - Sudden bursts
- **Soak test** - Extended duration

## Metrics to Capture
- Response time (p50, p95, p99)
- Throughput (req/sec)
- Error rate
- Concurrent users
- Resource utilization

## Example k6 Script
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 100,
  duration: '30s',
};

export default function () {
  const res = http.get('https://api.example.com/');
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(1);
}
```

---

## Caching Strategy Skill

```markdown
---
name: caching-strategy
description: Design effective caching
---

# Caching Strategies

## Cache Patterns

### Cache-Aside
1. Check cache
2. If miss, fetch from source
3. Store in cache
4. Return data

### Write-Through
1. Write to cache
2. Cache writes to source
3. Consistent but slower writes

### Write-Behind
1. Write to cache
2. Async write to source
3. Faster but eventual consistency

### Read-Through
1. Request from cache
2. Cache fetches on miss
3. Returns data

## Cache Invalidation
- **TTL** - Time-based expiration
- **Event-based** - Invalidate on changes
- **Manual** - Explicit invalidation
- **LRU** - Least recently used eviction

## Redis Caching Example
// Set with TTL
await redis.setex('user:123', 3600, JSON.stringify(user));

// Get with fallback
const cached = await redis.get('user:123');
if (cached) return JSON.parse(cached);
```

---

## Performance Patterns

### Lazy Loading
```javascript
// Only load when needed
const heavyModule = async () => {
  const module = await import('./heavy-module');
  return module.default;
};
```

### Debouncing
```javascript
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}
```

### Connection Pooling
```python
# SQLAlchemy pool
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)
```

---

## Performance Commands

### perf-audit.md
```markdown
Perform performance audit:
1. Run Lighthouse (if web)
2. Profile CPU and memory
3. Identify bottlenecks
4. Prioritize fixes by impact
5. Generate report
```

### benchmark.md
```markdown
Create benchmarks for function:
1. Write benchmark test
2. Run multiple iterations
3. Calculate statistics
4. Compare with baseline
```

---

## MCP Servers for Performance

| Server | Purpose |
|--------|---------|
| **Lighthouse MCP** | Web performance audits |
| **APM MCP** | Application monitoring |
| **Database MCP** | Query analysis |

---

## Resources

- [web.dev Performance](https://web.dev/performance/)
- [High Performance Browser Networking](https://hpbn.co/)
- [Systems Performance](https://www.brendangregg.com/systems-performance-2nd-edition-book.html) - Brendan Gregg
- [k6 Documentation](https://k6.io/docs/)
