> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# k2-fsa/sherpa-onnx — In Plain Language

## What is this about?

Think of sherpa-onnx as a toolbox that lets a device hear and speak
entirely on its own, with no cloud server involved.

One library covers a whole shelf of voice jobs: turning speech into text,
turning text back into speech, telling speakers apart, answering
"who spoke when," checking a claimed voice, guessing the spoken language,
labeling sounds, noticing when someone is talking, listening for a
wake word, adding punctuation, cleaning up noisy audio, and splitting
mixed sound into parts.

It handles both live and after-the-fact speech recognition. Live mode
transcribes as you talk, like captions. File mode waits for the whole
recording and then produces the result.

Named helpers inside include silero-vad for noticing speech, gtcrn and
DPDFNet for cleaning up audio, and spleeter and UVR for splitting
sources apart.

In short: download the library plus a model file, and your app can
listen, understand, and talk without sending audio anywhere.

## Why does it matter?

Most voice features today mean shipping your microphone audio to
someone else's server.

That brings three headaches: privacy risk, a bill for every minute,
and total failure when the network drops.

Running everything locally sidesteps all three. A meeting recorder,
a child's toy, a factory controller, or a voice remote can keep
working offline, with the audio never leaving the room.

It also matters because of breadth. Instead of learning a different
tool for each job or each device, one stack covers a dozen speech
tasks across phones, desktops, tiny boards, and browsers.

That lowers the cost of trying voice features: the same idea can be
tested in a browser demo and then shipped on a phone or an edge board.

## How does it work?

Picture three layers working together.

At the bottom is a model runner called ONNX Runtime. A model file is a
big bundle of numbers learned during training. The runner executes it
efficiently on whatever chip is available: a regular CPU, a graphics
chip, or a special AI accelerator.

In the middle is sherpa-onnx itself. It wraps that runner with a ready
recipe for each task: one recipe for live dictation, another for reading
text aloud, another for "who spoke when," and so on.

At the top are your model choice and a few lines of app code. You pick
the model for your task, drop it next to your program, and call the
library. Twelve programming languages are supported, including C++,
C, Python, Go, C#, Java, Kotlin, JavaScript, Swift, Rust, Dart, and
Object Pascal, plus WebAssembly for the browser.

Under the hood, one shared core written in C and C++ does the real work.
A single version number pins each release, and simple on/off switches
choose which features get built: Python bindings, text-to-speech,
diarization, the C interface, networking, graphics-chip support, or a
specific accelerator backend.

A matching set of build scripts then compiles that same core for each
target: four phone processor types for Android, simulator and device
slices for iOS, universal builds for macOS, HarmonyOS variants,
small-Linux boards with ARM and RISC-V chips, and separate WebAssembly
profiles for each task. Accelerator support for Rockchip, Qualcomm,
Ascend, Axera, and Intel chips plugs in the same way.

## Where can this be used?

Anywhere a device should hear or speak without phoning home.

On everyday computers and phones: offline dictation, subtitles for a
recorded video, a reader that speaks text aloud, or tagging what sound
just happened.

In shared conversations: marking which speaker said what, checking
whether this really is a known voice, or identifying the language
being spoken.

In noisy or mixed audio: stripping background hiss, or splitting a
voice track away from background music.

For hands-free control: a wake word that wakes the device, plus a
speech detector that tells the recognizer when to listen and when
to stay quiet so it does not waste battery.

On small and special hardware: the supported list names Raspberry Pi,
NVIDIA Jetson boards, RK3588, RV1126, LicheePi4A, VisionFive 2, and
SpacemiT boards, plus Android watches, iPhones, HarmonyOS devices,
desktop apps built with Flutter or Tauri, and web pages through
WebAssembly.

## Conclusions & takeaways

The big idea is simple: good speech tools should be boring to deploy,
private by default, and the same everywhere.

Sherpa-onnx bets that one offline stack with many tasks, many chips,
many operating systems, and many programming languages beats a patchwork
of cloud services tied to one vendor.

For a non-expert, the takeaway is: your device can already listen,
identify, clean up, and speak without the internet, once the right
model file is bundled with it.

For a builder, the takeaway is practical: pick the task, pick the
smallest model that fits your device, flip on only the build switches
you need, and run the matching build script for your target.

The trade-off is that portability takes work: each chip, store, and
browser needs its own build, which is why the project carries so many
build scripts and a strict release process.

## Jargon decoder

| Term | What it really means |
|---|---|
| Speech-to-text | Turning spoken words into written text, like dictation or captions. |
| Streaming vs. non-streaming | Live word-by-word results versus waiting for the whole file first. |
| Text-to-speech | Turning written text into a spoken voice, like a reader aloud. |
| Speaker diarization | Answering "who spoke when" in a recording with several people. |
| Speaker identification / verification | Guessing which known voice this is, or checking a claimed identity. |
| VAD (voice activity detection) | Noticing speech versus silence so the rest only runs when needed. |
| Speech enhancement | Removing noise and echo so a rough recording sounds clean. |
| Source separation | Splitting mixed audio apart, e.g. voice versus background music. |
| ONNX Runtime | A free engine that runs trained model files fast on many chips. |
| NPU (neural processing unit) | A small extra chip built to run AI math quickly on little power. |
