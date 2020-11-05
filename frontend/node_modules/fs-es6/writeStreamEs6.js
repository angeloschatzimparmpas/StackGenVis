import stream from 'stream'

export default class WriteStreamEs6 extends stream.Writable {
  constructor(writer, options) {
    super(options)

    this.writer = writer
  }

  async _write(chunk, enc, next) {
    const file = await this.writer
    await file.write(this._createBlob(chunk))
    next()
  }

  _createBlob(buffer) {
    const buf = new Buffer(buffer.byteLength)
    for (let i = 0; i < buf.length; ++i)
      buf[i] = buffer[i]

    return new Blob([buf])
  }
}
