//
// Copyright (c) 2012-2021 Snowflake Computing Inc. All right reserved.
//

#ifndef PC_PYTHON_COMMON_HPP
#define PC_PYTHON_COMMON_HPP

#include <Python.h>
#include "Util/macros.hpp"

namespace sf
{

namespace py
{
inline bool checkPyError()
{
  return UNLIKELY(PyErr_Occurred());
}

/**
 * A RAII class to wrap the PyObject*. The semantics are like std::unique_ptr.
 */
class UniqueRef
{
public:
  UniqueRef(const UniqueRef&) = delete;
  UniqueRef& operator=(const UniqueRef&) = delete;

  UniqueRef() : m_pyObj(nullptr)
  {
  }

  explicit UniqueRef(PyObject* pyObj) : m_pyObj(pyObj)
  {
  }

  explicit UniqueRef(UniqueRef&& other) : UniqueRef(other.release())
  {
  }

  UniqueRef& operator=(UniqueRef&& other)
  {
    reset(other.release());
    return *this;
  }

  ~UniqueRef()
  {
    reset();
  }

  void reset(PyObject* pyObj = nullptr)
  {
    Py_XDECREF(m_pyObj);
    m_pyObj = pyObj;
  }

  PyObject* release() noexcept
  {
    PyObject* tmp = m_pyObj;
    m_pyObj = nullptr;
    return tmp;
  }

  PyObject* get() const noexcept
  {
    return m_pyObj;
  }

  bool empty() const noexcept
  {
    return m_pyObj == nullptr;
  }

private:
  PyObject* m_pyObj;
};

/**
 * A RAII class to help us acquire the python GIL. The semantics are like
 * std::unique_lock.
 * We have to acquire the python GIL every time we call a Python/C API to ensure
 * there is only one python thread running all the time.
 */
class PyUniqueLock
{
public:
  PyUniqueLock(const PyUniqueLock&) = delete;
  PyUniqueLock& operator=(const PyUniqueLock&) = delete;
  PyUniqueLock(PyUniqueLock&&) = delete;
  PyUniqueLock& operator=(PyUniqueLock&&) = delete;

  PyUniqueLock()
  {
    m_state = PyGILState_Ensure();
  }

  ~PyUniqueLock()
  {
    PyGILState_Release(m_state);
  }

private:
  PyGILState_STATE m_state;
};

}  // namespace py
}  // namespace sf

#endif  // PC_PYTHON_COMMON_HPP
