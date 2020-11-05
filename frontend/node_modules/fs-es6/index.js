import 'babel-polyfill'
import FileSystemSync from './fileSystemSync'
import WriteStreamEs6 from './writeStreamEs6'

class FsEs6 {
  constructor(type, size) {
    this.fs = new FileSystemSync(type, size)
  }

  static create(type, size) {
    return new FsEs6(type, size)
  }

  writeFile(file, data, callback) {
    this.fs.getFileWriter(file)
      .then(writer => {
        this._write(writer, data)
        callback()
      })
      .catch(callback)
  }

  writeFileSync(file, data) {
    return this.fs.getFileWriter(file)
      .then(writer => this._write(writer, data))
  }

  appendFile(file, data, callback) {
    this.fs.getFileWriter(file, {create: false})
      .then(writer => {
        writer.seek(writer.length)
        this._write(writer, data)
        callback()
      })
      .catch(callback)
  }

  appendFileSync(file, data) {
    return this.fs.getFileWriter(file, {create: false})
      .then(writer => {
        writer.seek(writer.length)
        this._write(writer, data)
      })
  }

  readFile(file, callback) {
    this.fs.getFileReader(file)
      .then(reader => callback(null, reader.result))
      .catch(callback)
  }

  readFileSync(file) {
    return this.fs.getFileReader(file)
      .then(reader => reader.result)
  }

  unlink(path, callback) {
    this.fs.getFileEntry(path)
      .then(file => file.remove(callback, callback))
      .catch(callback)
  }

  unlinkSync(path) {
    return new Promise((resolve, reject) => {
      this.fs.getFileEntry(path)
        .then(file => file.remove(resolve, reject))
        .catch(reject)
    })
  }

  readdir(path, callback) {
    this.fs.getDirectoryEntry(path)
      .then(directory => this._getFiles(directory.createReader()))
      .then(files => callback(null, files))
      .catch(callback)
  }

  readdirSync(path) {
    return this.fs.getDirectoryEntry(path)
      .then(directory => this._getFiles(directory.createReader()))
  }

  mkdir(path, callback) {
    this.fs.getDirectoryEntry(path, {create: true})
      .then(() => callback())
      .catch(callback)
  }

  mkdirSync(path) {
    return this.fs.getDirectoryEntry(path, {create: true})
  }

  rmdir(path, callback) {
    this.fs.getDirectoryEntry(path)
      .then(directory => directory.removeRecursively(callback, callback))
      .catch(callback)
  }

  rmdirSync(path) {
    return new Promise((resolve, reject) => {
      return this.fs.getDirectoryEntry(path)
        .then(directory => directory.removeRecursively(resolve, reject))
        .catch(reject)
    })
  }

  exists(path, callback) {
    this.fs.getFileEntry(path)
      .then(() => callback(true))
      .catch(() => this.fs.getDirectoryEntry(path)
        .then(() => callback(true))
        .catch(() => callback(false)))
  }

  existsSync(path) {
    return this.fs.getFileEntry(path)
      .then(() => true)
      .catch(() => this.fs.getDirectoryEntry(path)
        .then(() => true)
        .catch(() => false))
  }

  access(path, callback) {
    this.fs.getFileEntry(path)
      .then(() => callback())
      .catch(() => this.fs.getDirectoryEntry(path)
        .then(() => callback())
        .catch(callback))
  }

  accessSync(path) {
    return this.fs.getFileEntry(path)
      .then(() => null)
      .catch(() => this.fs.getDirectoryEntry(path)
        .then(() => null))
  }

  stat(path, callback) {
    this.fs.getFileEntry(path)
      .then(file => file.getMetadata(callback.bind(this, null), callback))
      .catch(() => this.fs.getDirectoryEntry(path)
        .then(directory => directory.getMetadata(callback.bind(this, null), callback))
        .catch(callback))
  }

  statSync(path) {
    return new Promise((resolve, reject) => {
      this.fs.getFileEntry(path)
        .then(file => file.getMetadata(resolve, reject))
        .catch(() => this.fs.getDirectoryEntry(path)
          .then(directory => directory.getMetadata(resolve, reject))
          .catch(reject))
    })
  }

  // Verify if this method works as the same counterpart in node.js
  createWriteStream(path, options) {
    const promise = this.fs.getFileWriter(path)
    promise.then(file => file.truncate())
      .catch(error => Promise.reject({path, error}))

    return new WriteStreamEs6(promise, options)
  }

  _write(file, data) {
    if (!data)
      return

    if (typeof data === 'string')
      return file.write(new Blob([data], {type: 'text/plain'}))

    file.write(data)
  }

  _getFiles(directory) {
    let files = []
    const getFiles = (resolve, reject) => {
      directory.readEntries(results => {
        if (!results.length) {
          resolve(files.sort())
        }
        else {
          files = Array.prototype.slice.call(results, 0).concat(files)
          getFiles(resolve, reject)
        }
      }, reject)
    }

    return new Promise(getFiles)
  }
}

module.exports = new FsEs6()
