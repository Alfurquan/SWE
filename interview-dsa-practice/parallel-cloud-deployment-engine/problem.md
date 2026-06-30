# The Cloud Deployment Engine

We are building a deployment engine for cloud infrastructure (similar to Azure Resource Manager). A user submits a set of resources to provision. Some resources depend on others—for example, a Virtual Machine may depend on a Subnet, which itself depends on a Virtual Network.

The deployment engine should determine a **valid deployment order** such that every resource is deployed only after all of its dependencies have been successfully provisioned.

## Input Resources

| Resource | Dependencies |
|-----------|--------------|
| VM | Subnet |
| Subnet | VNet |
| StorageAccount | None |
| VNet | None |

## One Possible Deployment Plan

```text
[StorageAccount, VNet, Subnet, VM]
```

Describe and implement a solution that produces such a deployment plan.

---

### Follow-up Questions

1. How would your solution detect and handle circular dependencies?
2. What data structures would you use to represent the resources and their dependencies?
3. What are the time and space complexities of your approach?
4. How could the deployment engine maximize parallelism while respecting dependencies?
5. Suppose resources can be added dynamically while deployments are in progress. How would your design change?
6. How would you handle deployment failures and retries?
7. If deterministic output is required, how would you ensure the same deployment order is produced every time?
```