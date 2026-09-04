## Part 1: Standalone Hardware Options

**ESP32 / ESP32-S3 (using esp-csi)** ~500–550 EGP or ~1,250–1,950 EGP
This is Espressif's own official CSI toolkit, actively maintained and supported across their entire chip lineup (ESP32, ESP32-S2, C3, S3, C5, C6, C61). It's a low-cost microcontroller that can extract CSI from WiFi frames it receives, either passively (sniffing ambient traffic) or actively (pinging a router and reading the CSI in the reply). In practice it delivers roughly 128 usable subcarriers due to UART throughput limits, over 20/40 MHz bandwidth.
- *Pros:* Extremely cheap ($5–15/board), tiny form factor, easy to deploy several units for spatial coverage, actively developed by the chip manufacturer itself, capable of on-device processing/ML, well-documented for beginners.
- *Cons:* Lower subcarrier resolution than PC-hosted tools, UART bottleneck limits practical subcarrier count well below the chip's theoretical maximum, less mature research literature to benchmark against compared to Intel/Atheros tools.

**ESP32-C5 "esp-crab" (dual-chip phase-sync board)** Unknown — would need import
A specialized Espressif reference design using two co-crystal ESP32-C5 chips that share a clock source, purpose-built for high-precision phase-based sensing (e.g., detecting millimeter-level RF disturbances). It supports both self-transmit/self-receive and single-transmit/dual-receive configurations.
- *Pros:* Solves the hard problem of phase synchronization at the hardware level, useful if precise angle-of-arrival or fine-grained triangulation becomes a project goal, still built on the affordable ESP32 platform.
- *Cons:* Newer and less documented than mainstream ESP32 CSI tools, more complex to set up, likely unnecessary for our project since we're planning to rely on amplitude-based localization rather than phase-based methods.

**Raspberry Pi 4B + Nexmon CSI** ~4,500–7,700 EGP
Nexmon is a firmware-patching framework that enables CSI extraction on the Raspberry Pi's built-in Broadcom WiFi chip (BCM43455c0). It supports up to 80 MHz bandwidth and up to 242 subcarriers in theory, though real-world literature suggests only about 114 of those are actually useful for activity recognition.
- *Pros:* Reasonable resolution, runs full Linux (making custom data pipelines and synchronization logic easier to implement), inexpensive relative to PC-hosted NIC tools, well-known in the WiFi sensing community.
- *Cons:* CSI data quality has been reported as noisier than Intel 5300 or Atheros alternatives, historically required older, specific Linux kernel versions (up to 5.4) making system updates risky, single antenna on the Pi limits MIMO configurations, kernel/firmware compatibility can break unexpectedly.

**Intel 5300 NIC (Linux 802.11n CSI Tool)** Must import via eBay (~$15–40 + shipping + customs)
This is the most historically significant CSI research tool, built on Intel's WiFi Link 5300 802.11n MIMO radio with custom firmware and Linux drivers. It reports CSI across 30 subcarrier groups (one per ~2 subcarriers at 20 MHz, or ~4 at 40 MHz).
- *Pros:* By far the most cited and well-understood tool in the CSI research literature (including the Tokunaga et al. paper we reviewed), extremely well-documented, highly stable once set up correctly.
- *Cons:* Discontinued hardware, released in 2008 — genuinely difficult to source in 2026; requires an equally old laptop/desktop chassis compatible with the card; low subcarrier count (only 30 groups) may be insufficient for our localization goals; firmware and drivers built for old OS versions, creating compatibility headaches on modern systems.

**Atheros CSI Tool (QCA9300 / AR9300-class chipsets)** Must import via eBay (~$20–50 + shipping + customs)
An open-source measurement tool for Qualcomm Atheros WiFi chipsets, delivering higher resolution than Intel 5300 — 56 subcarriers at 20 MHz or 114 at 40 MHz. This is the tool used to build the NTU-Fi datasets referenced in the SenseFi benchmark paper.
- *Pros:* Higher subcarrier resolution than Intel 5300, still available for purchase as mini-PCIe cards, directly relevant to the SenseFi benchmark our professor pointed us to, reasonably well-documented.
- *Cons:* Each receiver node requires a full PC or laptop with a mini-PCIe slot (not a standalone microcontroller), making multi-node deployment expensive and physically bulky; less actively maintained than newer tools like PicoScenes; driver setup still involves patched firmware.

**PicoScenes (modern multi-chipset middleware; supports AX210, AX200, QCA9300, IWL5300, or SDR)**
PicoScenes is a actively-developed, modern CSI extraction platform that supports the newest WiFi standards (802.11ax) on commodity Intel AX210/AX200 NICs, in addition to legacy Atheros and Intel 5300 hardware. It can extract CSI up to 160 MHz bandwidth and can passively harvest CSI from any overheard WiFi frame in the environment, not just frames it specifically requested.
- *Pros:* Most future-proof and actively maintained of the PC-hosted options, supports the widest range of hardware and WiFi standards, best documentation among the "modern" tools, cards (like AX210) are cheap and easy to buy new.
- *Cons:* Still requires one PC/laptop per receiver node like Atheros/Intel 5300, heavier and more complex software stack, less beginner-friendly to set up than ESP32.

**Software-Defined Radio (USRP / HackRF, via PicoScenes)**
SDRs provide access to raw radio signal data rather than pre-processed CSI, giving complete flexibility over bandwidth, protocol, and signal processing at the cost of significant complexity.
- *Pros:* Maximum possible flexibility and signal resolution, fully research-grade, no dependency on any single WiFi chipset's limitations.
- *Cons:* Expensive (USRP models run $700–3000+, HackRF around $300), steep RF engineering learning curve, almost certainly overkill and impractical for a one-year student graduation project.

## Part 2: Hybrid Hardware Possibilities

**All-ESP32 Array (3–5 ESP32-S3 nodes + 1 router as TX)** ~2,100 EGP
Every receiver in the room is an ESP32 board running esp-csi, spread out for spatial diversity, all reporting to the laptop over serial or WiFi.
- *Pros:* Cheapest possible option for a multi-node array, easiest to physically deploy and reposition since each node is small and self-contained, consistent hardware across all nodes simplifies software/sync work, scales easily if we decide we need more nodes later.
- *Cons:* Every node shares the same subcarrier/resolution ceiling (~128 usable subcarriers), so we sacrifice per-node data richness in exchange for spatial coverage; less established research precedent for localization-grade accuracy compared to Atheros/Intel-based work.

**All-Raspberry Pi Array (3–4 Pi 4B units, each running Nexmon)** ~22,000 EGP
Every receiver is a full Raspberry Pi running Nexmon CSI, each with its own SD card, OS, and network connection.
- *Pros:* Higher per-node resolution than ESP32 (up to ~114-242 usable subcarriers), full Linux environment on every node gives more flexibility for custom preprocessing or synchronization logic at the edge, single antenna keeps the setup relatively simple per node.
- *Cons:* Bulkier and more expensive per node than ESP32 (~$35–55+ per Pi versus $5-15 per ESP32), reported CSI noise issues compound across multiple nodes, kernel-version fragility becomes a bigger risk when multiplied across several independently-managed Linux devices, more moving parts to keep synchronized and powered.

**Hybrid: One High-Resolution Node (Atheros or PicoScenes/AX210) + Multiple ESP32 Nodes**
One "anchor" receiver using a higher-resolution PC-hosted tool provides a strong reference stream, while 2–4 cheap ESP32 nodes are placed around the room purely for spatial diversity and localization triangulation.
- *Pros:* Combines the best of both worlds — one data stream with research-grade resolution (useful for validating our results against literature like the SenseFi benchmark and Tokunaga paper) while still getting the spatial coverage needed for localization at low cost; keeps overall budget and physical footprint manageable since we only need one extra laptop/PC instead of three or four.
- *Cons:* Introduces hardware heterogeneity, meaning our preprocessing pipeline must handle two very different CSI formats, subcarrier counts, and noise profiles simultaneously; synchronization becomes more complex since the anchor node and the ESP32 nodes may have different native timing behavior and drivers; fusing data of meaningfully different quality/resolution into one model requires careful feature engineering or normalization.

**Hybrid: Raspberry Pi (Nexmon) as Anchor + ESP32 Nodes for Spatial Coverage**
Similar structure to the above, but using a Raspberry Pi instead of an Atheros/PicoScenes PC as the anchor node, paired with several ESP32s for localization.
- *Pros:* Lower cost than the PC-based anchor hybrid above since a Pi is cheaper than a full laptop with a mini-PCIe NIC; still gains a meaningfully higher-resolution central stream than an all-ESP32 setup; both anchor and satellite nodes run comparatively lightweight embedded software, which may simplify deployment logistics.
- *Cons:* The anchor node inherits Nexmon's known noise concerns, meaning even our "best" data stream isn't as clean as an Atheros/Intel-based anchor would be; still requires managing two different hardware/software stacks (Pi + ESP32) for synchronization and preprocessing; kernel-version fragility on the Pi remains a risk for the one node we're relying on most heavily.

**Hybrid: Mixed Atheros/PicoScenes Nodes (2+ PC-hosted receivers, no ESP32)**
Multiple higher-resolution nodes (e.g., 2–3 Atheros or AX210 cards), each requiring its own PC or laptop, positioned around the room.
- *Pros:* Highest overall data quality and consistency across all nodes since every stream uses the same, well-resolved CSI format; avoids the complexity of fusing heterogeneous hardware; aligns closely with the SenseFi benchmark's data collection approach, making cross-validation against published results more straightforward.
- *Cons:* Most expensive and logistically difficult hybrid option, since each node needs a dedicated PC or laptop rather than a cheap microcontroller — likely impractical for a 3–4 node localization array on a student budget; hardest to physically position flexibly around a room compared to small ESP32 boards; scaling up node count later is costly.