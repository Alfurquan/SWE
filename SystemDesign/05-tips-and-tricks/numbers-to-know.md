# Numbers to Know

## Mordern Hardware limits

Modern servers pack serious computing power. An AWS M6i.32xlarge comes with 512 GiB of memory and 128 vCPUs for general workloads. Memory-optimized instances go further: the X1e.32xlarge provides 4 TB of RAM, while the U-24tb1.metal reaches 24 TB of RAM. This shift matters because many applications that once required distributed systems can now run on a single machine.
Storage capacity has seen similar growth. Modern instances like AWS's i3en.24xlarge provide 60 TB of local SSD storage. If you need more, the D3en.12xlarge offers 336 TB of HDD storage for data-heavy workloads. Object storage like S3 is effectively unlimited, handling petabyte-scale deployments as a standard practice. The days of storage being a primary constraint are largely behind us.
Network capabilities haven't stagnated either. Within a datacenter, 10-25 Gbps is common, with high-performance instances supporting 50-100 Gbps or more. Cross-zone bandwidth within a region is typically limited only by instance network capacity. Latency remains predictable: 1-2ms within a region, and 50-150ms cross-region. This consistent performance allows for reliable distributed system design.
These aren't just incremental improvements – they represent a step change in what's possible. When textbooks talk about splitting databases at 100GB or avoiding large objects in memory, they're working from outdated constraints. The hardware running our systems today would have been unimaginable a decade ago, and these capabilities fundamentally change how we approach system design.

## Applying These Numbers in System Design Interviews

Let's look at how these numbers impact specific components and the decisions we make when designing systems in an interview.


| Component        | Key Metrics                                                                 | Scale Triggers                                                                 |
|------------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| Caching          | ~1 millisecond latency<br>100k+ operations/second<br>Memory-bound (up to 1TB) | Hit rate < 80%<br>Latency > 1ms<br>Memory usage > 80%<br>Cache churn/thrashing |
| Databases        | Up to 50k transactions/second<br>Sub-5ms read latency (cached)<br>64 TiB+ storage capacity | Write throughput > 10k TPS<br>Read latency > 5ms uncached<br>Geographic distribution needs |
| App Servers      | 100k+ concurrent connections<br>8–64 cores @ 2–4 GHz<br>64–512GB RAM standard, up to 2TB | CPU > 70% utilization<br>Response latency > SLA<br>Connections near 100k/instance<br>Memory > 80% |
| Message Queues   | Up to 1M msgs/sec per broker<br>Sub-5ms end-to-end latency<br>Up to 50TB storage | Throughput near 800k msgs/sec<br>Partition count ~200k per cluster<br>Growing consumer lag |

