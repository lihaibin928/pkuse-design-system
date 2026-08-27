import { useState } from 'react';

export function useBoolean(initValue = false) {
  const [bool, setBool] = useState(initValue);

  function setTrue() {
    setBool(true);
  }

  function setFalse() {
    setBool(false);
  }

  function toggle() {
    setBool(!bool);
  }

  return {
    bool,
    setBool,
    setTrue,
    setFalse,
    toggle,
  };
}
