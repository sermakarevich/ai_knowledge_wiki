> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Appendix: Example Payloads
**In one sentence:** The curator synthesizes task-specific guidance from retrieved trajectories, shown in one example payload per benchmark plus GRPO training curves where validation success rises and executor turns fall over 100 steps.
## Key points
- One curated payload is shown per benchmark, each pairing a task with the payload the curator synthesized from retrieved trajectories.
- On ALFWorld (Clean: "Put a clean plate in countertop"), the payload assembles a clean-and-place procedure from three partially relevant episodes (cooled plate, cleaned tomato, cleaned soapbar).
- The ALFWorld payload gives a 3-step strategy (locate plate on countertops, clean in sinkbasin, place on countertop) and 4-step specific guidance (go to countertop 1 or 2, take plate, clean at sinkbasin, return and place).
- On WebShop ("high speed flashes with usb port, usb256-pink, 512gb, under $40"), the payload converts searches for different products (men's t-shirts, gym shorts) into a search-phrasing and attribute-selection strategy for the current product.
- The WebShop payload prescribes precise search phrasing including product type, features, color, size, and price; exact color/size clicks ("usb256-pink", "512gb"); and price verification before purchase.
- On τ2-bench Telecom (unable to send MMS), the payload distills several MMS failure cases (Memories 1 and 3 same issue with travel/roaming and data-cap blockage; Memory 2 domestic app-permission/network-mode fix) into an ordered diagnostic procedure separating general resolution strategy from current-request guidance.
- The τ2-bench payload orders diagnosis as identify line, gather device/network state first, apply non-account fixes in order, check account-side blockers only after, and requires explicit user approval with confirmed amount/charge before the mutating `refuel_data` tool; it also warns not to assume line ID, roaming status, or data usage from memory.
- Figures 5 and 6 show GRPO training progress on ALFWorld and WebShop (Qwen3-8B executor) over 100 steps: validation success rate climbs steadily while executor turns per task fall, with stable training under a single task reward and no auxiliary content-quality reward, task grouping, or return shaping.
---
## Overview
**Covers:** appendix pp. 22–25, example payloads intro

Across all three benchmarks, the curator produces task-specific guidance from retrieved trajectories. On ALFWorld, it assembles a clean-and-place procedure from three partially relevant episodes. On WebShop, it converts searches for different products into a search-phrasing and attribute-selection strategy for the current one. On τ2-bench, it distills several MMS failure cases into an ordered diagnostic procedure, separating a general resolution strategy from guidance specialized to the current request. Notably, the curator carries over the domain policy that the mutating tool requires explicit user approval.

## ALFWorld payload (Task type: Clean)
**Covers:** appendix p. 22, ALFWorld example

Task: Put a clean plate in countertop

Briefing for Task: Put a clean plate in countertop

Relevant Memories:
- Memory 1: Successfully cooled and placed a plate on a countertop.
- Memory 2: Cleaned and placed a tomato on a countertop.
- Memory 3: Cleaned and placed a soapbar in a toilet (cleaning process is similar).

Key Strategies:
1. Locate the plate: Check countertops first, as plates are often found there.
2. Clean the plate: Use a sinkbasin to clean it if it's dirty.
3. Move the plate: Once clean, place it on a desired countertop.

Specific Guidance:
1. Go to a countertop (e.g., countertop 1 or 2) to find the plate.
2. Take the plate from the countertop.
3. Go to the sinkbasin and clean the plate if it's dirty.
4. Return to a countertop and place the clean plate there.

## WebShop payload
**Covers:** appendix pp. 22–23, WebShop example

Task: Find me high speed flashes with usb port with color: usb256-pink, and size: 512gb, and price lower than 40.00 dollars.

Target Product: High speed flashes with usb port, color: usb256-pink, size: 512gb, price lower than $40.00

Relevant Past Experiences:
- Memory 1 and Memory 2 involved searching for men's t-shirts with specific color and size constraints, and included steps to select the correct color and size options.
- Memory 3 involved searching for men's gym shorts with specific color and size constraints, and included steps to select the correct color and size options.

Strategies from Past Experiences:
1. Search Phrasing: Use precise search terms that include the product type, key features, color, size, and price constraint. For example, "high speed flashes with usb port usb256-pink 512gb under $40".
2. Color Selection: Click on the exact color option from the color palette to select the desired color.
3. Size Selection: Click on the exact size option from the size options to select the desired size.
4. Price Constraint: Ensure the final product price is within the specified budget before purchasing.

Actionable Guidance:
1. Search: Begin with a search query that includes the product type, key features, color, size, and price constraint. For example, "high speed flashes with usb port usb256-pink 512gb under 40".
2. Navigate Results: Click on the product that matches your criteria.
3. Select Color: From the color options, click on "usb256-pink".
4. Select Size: From the size options, click on "512gb".
5. Verify Price: Ensure the final price is within the specified budget before proceeding to purchase.

## τ2-bench payload (Domain: Telecom)
**Covers:** appendix p. 23, τ2-bench example

Task: You are unable to send MMS messages using your messaging app for the past few hours. You want to fix it and successfully send an MMS message.

Most relevant memories: Memory 1 and Memory 3 (same MMS issue, including travel/roaming and possible data-cap blockage). Memory 2 is also useful for the domestic case where app permissions/network mode were the fix.

Resolution strategy that worked:
1. Identify the customer/line
   - Use 'get_customer_by_phone' (or equivalent customer lookup).
   - If multiple lines exist, confirm the exact phone number/line affected.
2. Gather device/network state first
   - Ask user to run/read: 'check_network_status', 'can_send_mms', 'check_apn_settings', 'check_wifi_calling_status', and app permission checks (use 'check_installed_apps' first if app name is unclear).
   - If abroad, specifically verify mobile data ON, data roaming ON, and usable network service (not airplane mode / no SIM / 2G-only).
3. Guide user through non-account fixes in order
   - If airplane mode is on: turn it off.
   - If SIM missing: reseat SIM.
   - If mobile data or roaming is off: turn them on.
   - If stuck on poor/2G service: set preferred network mode to '4g_5g_preferred'.
   - If messaging app lacks permissions: grant sms and storage.
   - If needed, check/reset APN and reboot.
   - If Wi-Fi Calling is on and MMS still fails, try turning it off.
4. Check account-side blockers only after device state is good
   - Look up the correct line with 'get_details_by_id'.
   - Verify line is active and whether roaming is enabled on the account.
   - Use 'get_data_usage' and plan lookup to see if the line is over its data limit.
5. If over data limit and MMS depends on mobile data
   - Explain the overage and available options.
   - Confirm allowed refuel amount and total charge.
   - Obtain explicit user approval.
   - Apply with 'refuel_data'.

Guidance for this request:
- Start by identifying the customer/line, then immediately collect current device state with: 'check_network_status', 'can_send_mms', 'check_apn_settings', 'check_wifi_calling_status', 'check_installed_apps' -> 'check_app_permissions' for the actual messaging app.
- Based on results, prioritize: (1) restore basic cellular service (airplane mode/SIM/signal/network mode), (2) ensure mobile data is enabled, (3) if roaming is relevant, ensure device roaming is on and account roaming is enabled, (4) fix app permissions ('sms', 'storage'), (5) APN reset/reboot if still failing.
- If the device shows good service/data and MMS still fails, check the account line and data usage; if at/over limit, offer a data refuel only after confirming price and receiving explicit approval before calling the mutating tool.
- Do not assume the same line ID, roaming status, or data usage from memory — look up the current case.

## Training curves (Figures 5 and 6)
**Covers:** appendix pp. 23–25, training curves

> "Training curves. Figures 5 and 6 show GRPO training progress on ALFWorld and WebShop, with validation on a subsampled test stream. On both benchmarks, validation success rate climbs steadily over 100 training steps while executor turns per task fall, indicating the curator learns to produce payloads that improve task success while reducing the number of executor steps. Training is stable throughout under a single task reward, with no auxiliary content-quality reward, no task grouping, and no return shaping — supporting the claim that read-time curation makes curator learning straightforward."

- Figure 5: GRPO training curves on ALFWorld (Qwen3-8B executor). Top row: training SR and executor turns. Bottom row: the same metrics on validation. SR rises and turns fall steadily over 100 steps.
- Figure 6: GRPO training curves on WebShop (Qwen3-8B executor). Top row: training SR, training score, training executor turns. Bottom row: the same three metrics on validation.
