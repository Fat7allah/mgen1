const path = require('path');
const esbuild = require('esbuild');

const APPS_PATH = path.resolve(__dirname, '..', '..', 'apps');
const APP_NAME = 'mgen1';
const APP_PATH = path.resolve(APPS_PATH, APP_NAME);
const JS_PATH = path.resolve(APP_PATH, APP_NAME, 'public/js');
const CSS_PATH = path.resolve(APP_PATH, APP_NAME, 'public/css');

// Get all JavaScript files
const js_files = [
  path.resolve(JS_PATH, 'المصارف.js'),
  path.resolve(JS_PATH, 'المداخل.js')
];

// Build options
const options = {
  entryPoints: js_files,
  bundle: true,
  outdir: path.resolve(APP_PATH, APP_NAME, 'public/dist'),
  sourcemap: true,
  minify: process.argv.includes('--production'),
  target: ['es2017'],
  loader: {
    '.js': 'jsx'
  }
};

// Build process
async function build() {
  try {
    await esbuild.build(options);
    console.log('Build completed successfully');
  } catch (err) {
    console.error('Build failed:', err);
    process.exit(1);
  }
}

build();
