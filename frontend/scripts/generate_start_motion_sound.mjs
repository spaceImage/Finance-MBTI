import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const sampleRate = 44100;
const durationSeconds = 1.82;
const frameCount = Math.ceil(sampleRate * durationSeconds);
const samples = new Float32Array(frameCount);

function addBoing(start, length, startFrequency, endFrequency, gain) {
  const startFrame = Math.floor(start * sampleRate);
  const endFrame = Math.min(frameCount, startFrame + Math.floor(length * sampleRate));
  let phase = 0;

  for (let frame = startFrame; frame < endFrame; frame += 1) {
    const progress = (frame - startFrame) / (endFrame - startFrame);
    const frequency =
      startFrequency * Math.pow(endFrequency / startFrequency, progress);
    phase += (Math.PI * 2 * frequency) / sampleRate;

    const attack = Math.min(1, progress / 0.035);
    const decay = Math.pow(1 - progress, 2.15);
    const wobble = 1 + 0.035 * Math.sin(Math.PI * 2 * 7.5 * progress);
    const fundamental = Math.sin(phase);
    const warmOvertone = 0.24 * Math.sin(phase * 2.01 + 0.35);

    samples[frame] +=
      gain * attack * decay * wobble * (fundamental + warmOvertone);
  }
}

addBoing(0.06, 0.66, 690, 260, 0.42);
addBoing(0.84, 0.82, 610, 205, 0.38);

const pcmBytes = frameCount * 2;
const wav = Buffer.alloc(44 + pcmBytes);
wav.write("RIFF", 0);
wav.writeUInt32LE(36 + pcmBytes, 4);
wav.write("WAVE", 8);
wav.write("fmt ", 12);
wav.writeUInt32LE(16, 16);
wav.writeUInt16LE(1, 20);
wav.writeUInt16LE(1, 22);
wav.writeUInt32LE(sampleRate, 24);
wav.writeUInt32LE(sampleRate * 2, 28);
wav.writeUInt16LE(2, 32);
wav.writeUInt16LE(16, 34);
wav.write("data", 36);
wav.writeUInt32LE(pcmBytes, 40);

for (let index = 0; index < frameCount; index += 1) {
  const softened = Math.tanh(samples[index] * 1.15) * 0.82;
  wav.writeInt16LE(Math.round(softened * 32767), 44 + index * 2);
}

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const outputPath = resolve(
  scriptDirectory,
  "../public/sounds/start-dotori-boing.wav",
);
mkdirSync(dirname(outputPath), { recursive: true });
writeFileSync(outputPath, wav);
console.info(`Generated ${outputPath}`);
