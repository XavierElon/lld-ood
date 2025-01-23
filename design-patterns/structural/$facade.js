/*
Facade

Summary
Provides a simplified interface to a complex subsystem. A facade offers a high-level interface that makes the subsystem easier to use.

When to use
	•	When you have a complex subsystem (many classes, APIs) that you want to hide behind a unified interface.
	•	To simplify usage of a library or subsystem for the client code.
*/

class VideoConverter {
  convert(filename, format) {
    // Complex subsystem calls
    const file = new File(filename)
    const sourceCodec = new CodecFactory().extract(file)
    const destinationCodec = format === 'mp4' ? new MPEG4Codec() : new OggCodec()
    const buffer = new BitrateReader().read(filename, sourceCodec)
    const result = new BitrateReader().convert(buffer, destinationCodec)
    // ...
    return new File(result)
  }
}

// Usage
const converter = new VideoConverter()
const mp4Video = converter.convert('myvideo.ogg', 'mp4')
