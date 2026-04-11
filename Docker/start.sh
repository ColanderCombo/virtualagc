#!/bin/bash
export PS_PERSONALITY=linux
set -e

echo "🚀 Starting X11 env..."

Xvfb :1 -screen 0 1600x900x24 &
export DISPLAY=:1

fluxbox &
x11vnc -display :1 -nopw -forever -shared -ncache 10 -noxdamage &
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &

sleep 5

echo "🧠 Generating a runtime..."

cd /opt/virtualagc/VirtualAGC

echo "📦 Verifying the runtime..."

SRC="/opt/virtualagc/VirtualAGC/temp/lVirtualAGC"
DST="/opt/virtualagc-dist"

if [ ! -d "$SRC" ]; then
  echo "❌ ERROR: $SRC does not exist"
  exit 1
fi

echo "🔁 Clean runtime for $DST..."

mkdir -p "$DST"

cp -r "$SRC/"* "$DST/"

echo "📁 Folder structure under dst:"
ls -lah "$DST/bin"

### Patch

echo "🔧 Validating SimStop..."

SIMSTOP_PATH=$(find /opt/virtualagc-dist -name SimStop | head -n 1)

if [ -z "$SIMSTOP_PATH" ]; then
  echo "❌ SimStop not found"
  exit 1
fi

echo "📍 SimStop found at: $SIMSTOP_PATH"

# Check if this is the legacy version
if grep -q "ps -U" "$SIMSTOP_PATH"; then
  echo "⚠️ Legacy version detected. Applying patch..."

  cat > "$SIMSTOP_PATH" << 'EOF'
#!/bin/bash
trap "" 0 1 2 9 15 17 19 23
sleep 5
echo "Scanning for program status of processes ${PIDS}"
running=1
while [ $running -eq 1 ]; do
  sleep 1
  for n in ${PIDS}; do
    if ! kill -0 "$n" 2>/dev/null; then
      echo "Process ${n} has terminated."
      running=0
      break
    fi
  done
done
echo "Bye! Shutting down the simulation."
for n in ${PIDS}; do
  kill "$n" 2>/dev/null
done
sleep 0.25
for n in ${PIDS}; do
  if kill -0 "$n" 2>/dev/null; then
    kill -KILL "$n" 2>/dev/null
  fi
done
EOF

  chmod +x "$SIMSTOP_PATH"

  echo "✅ Patch applied successfully"

else
  echo "✅ SimStop is already up-to-date. No patch needed."
fi

### End patch

echo "🚀 Starting VirtualAGC..."

cd "$DST/bin"

exec ./VirtualAGC
