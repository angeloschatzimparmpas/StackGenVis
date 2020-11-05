export default class fileWriterSync {
  constructor(writer, path) {
    this.writer = writer
    this.path = path
    this._stack = Promise.resolve()
  }

  get stack() {
    return this._stack
  }

  set stack(promise) {
    this._stack = promise
  }

  write(content) {
    return this._execute(this.writer.write, content)
  }

  async seek(position) {
    await this.stack
    this.writer.seek(position)
  }

  truncate(length) {
    return this._execute(this.writer.truncate, length)
  }

  _execute(action, data) {
    this.stack = this.stack.then(()=> {
      return new Promise((resolve, reject) => {
        this.writer.onwriteend = resolve
        this.writer.onerror = error => reject({path: this.path, error})
        action.call(this.writer, data)
      })
    })

    return this.stack
  }
}
