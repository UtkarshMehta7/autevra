import { useEffect, useState } from "react";
import type { DerivedValue, ParameterDef } from "../api/types";
import { formatValue } from "../state/format";

interface Props {
  parameters: ParameterDef[];
  values: Record<string, number>;
  derived: DerivedValue[];
  error: string | null;
  onSet: (parameter: string, value: number) => void;
}

const GROUPS: [string, string][] = [
  ["body", "Body"],
  ["interior", "Interior"],
  ["dimensions", "Dimensions"],
  ["cabin", "Cabin"],
  ["wheels", "Wheels & tyres"],
  ["steering", "Steering"],
  ["frame", "Chassis frame"],
  ["suspension", "Suspension"],
  ["mass", "Mass"],
  ["powertrain", "Powertrain & road loads"],
];

function ChoiceInput({ def, value, onSet }: {
  def: ParameterDef; value: number; onSet: (v: number) => void;
}) {
  return (
    <label className="param" title={def.description}>
      <span>{def.label}</span>
      <select value={Math.round(value)} onChange={(e) => onSet(Number(e.target.value))}>
        {def.options!.map((option, i) => <option key={option} value={i}>{option}</option>)}
      </select>
      <em />
    </label>
  );
}

function ParameterInput({ def, value, onSet }: {
  def: ParameterDef; value: number; onSet: (v: number) => void;
}) {
  if (def.options?.length) return <ChoiceInput def={def} value={value} onSet={onSet} />;
  return <NumberInput def={def} value={value} onSet={onSet} />;
}

function NumberInput({ def, value, onSet }: {
  def: ParameterDef; value: number; onSet: (v: number) => void;
}) {
  const [text, setText] = useState(String(value));
  useEffect(() => {
    setText(String(value));
  }, [value]);
  const commit = () => {
    const v = Number(text);
    if (text.trim() === "" || Number.isNaN(v)) return setText(String(value));
    if (v !== value) onSet(v);
  };
  return (
    <label className="param" title={`${def.description} (${def.min}–${def.max} ${def.unit})`}>
      <span>{def.label}</span>
      <input
        type="number"
        value={text}
        step={def.step}
        min={def.min}
        max={def.max}
        onChange={(e) => setText(e.target.value)}
        onBlur={commit}
        onKeyDown={(e) => e.key === "Enter" && (e.target as HTMLInputElement).blur()}
      />
      <em>{def.unit}</em>
    </label>
  );
}

export function PropertyEditor({ parameters, values, derived, error, onSet }: Props) {
  return (
    <section className="panel">
      <h2>Parameters</h2>
      {error && <div className="error">{error}</div>}
      {[...GROUPS, ...[...new Set(parameters.map((p) => p.group))]
        .filter((g) => !GROUPS.some(([k]) => k === g))
        .map((g) => [g, g.charAt(0).toUpperCase() + g.slice(1)] as [string, string])]
        .map(([group, label]) => (
        <fieldset key={group}>
          <legend>{label}</legend>
          {parameters.filter((p) => p.group === group).map((def) => (
            <ParameterInput key={def.id} def={def} value={values[def.id]}
              onSet={(v) => onSet(def.id, v)} />
          ))}
        </fieldset>
      ))}
      <fieldset>
        <legend>Derived (read-only)</legend>
        {derived.map((d) => (
          <div key={d.id} className="param derived" title={`from ${d.controlled_by.join(", ")}`}>
            <span>{d.label}</span>
            <output>{formatValue(d.value, d.unit)}</output>
          </div>
        ))}
      </fieldset>
    </section>
  );
}
