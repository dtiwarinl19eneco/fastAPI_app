**Trade-offs and improvements for the CI/CD**

**Trunk based deployments. I have implemented something similar in my previous organization and it worked great.

1. This is a single pipeline for CI/CD. For big organizations, we can split into separate CI and CD.
2. High security assurance. no vulnerable code merges.
3. Promotes exact same image across all the environments.
4. Reduces MTTR (mean time to recovery) after bad deploys.
5. Can also deploy extra security like cortex-agent(Palo alto antivirus) antivirus using helm(Did it in my past 
   experience).
6. Separate SPNs for each env.
6. Very large, might be difficult to maintain. So can split into reusable templates in Azure DevOps.
7. Use caching to reduce build times. Parallelize linting, tests, and scans.
8. Can also integrate regression and performance testing in the CI/CD pipeline(I did it in my previous work).
9. Introduce canary → traffic shaping (Azure Front Door / Istio / Flagger). Use feature flags (LaunchDarkly, Azure App 
   Configuration) to decouple deploy from release.
10. Add approvals and checks gates explicitly for pre-prod and Pro in Azure DevOps.