import numpy as np

def analyze_metrics(metrics):
    recs = []
    pods = metrics.get("pods", [])
    cpu_usages = [p["cpu_usage"] for p in pods]
    mem_usages = [p["mem_usage"] for p in pods]
    cpu_limits = [p["cpu_limit"] for p in pods]
    mem_limits = [p["mem_limit"] for p in pods]

    cpu_mean = np.mean(cpu_usages) if cpu_usages else 0
    cpu_std = np.std(cpu_usages) if cpu_usages else 0

    for pod in pods:
        if pod["cpu_usage"] < 0.3 * pod["cpu_limit"]:
            recs.append({
                "pod": pod["name"],
                "type": "over-provisioned",
                "suggestion": "Reduce CPU limit",
                "current_cpu": pod["cpu_usage"],
                "cpu_limit": pod["cpu_limit"]
            })
        elif pod["cpu_usage"] > 0.9 * pod["cpu_limit"]:
            recs.append({
                "pod": pod["name"],
                "type": "under-provisioned",
                "suggestion": "Increase CPU limit or enable autoscaling",
                "current_cpu": pod["cpu_usage"],
                "cpu_limit": pod["cpu_limit"]
            })
        if cpu_std > 0.2 * cpu_mean and pod["cpu_usage"] > 0.7 * pod["cpu_limit"]:
            recs.append({
                "pod": pod["name"],
                "type": "spiky-usage",
                "suggestion": "Enable HPA (Horizontal Pod Autoscaler)",
                "current_cpu": pod["cpu_usage"],
                "cpu_limit": pod["cpu_limit"]
            })
        if pod.get("qos_class") == "BestEffort" and pod["cpu_limit"] > 0:
            recs.append({
                "pod": pod["name"],
                "type": "qos",
                "suggestion": "Consider Burstable or Guaranteed QoS class",
                "current_qos": pod["qos_class"]
            })
        cost = estimate_cost(pod["cpu_limit"], pod["mem_limit"])
        recs.append({
            "pod": pod["name"],
            "type": "cost",
            "suggestion": f"Estimated monthly cost: ${cost:.2f}",
            "cpu_limit": pod["cpu_limit"],
            "mem_limit": pod["mem_limit"]
        })
    return recs

def estimate_cost(cpu, mem):
    return cpu * 10 + mem * 2.5 