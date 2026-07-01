import { defineConfig, globalIgnores } from 'eslint/config'
import globals from 'globals'
import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import tsParser from '@typescript-eslint/parser'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'

export default defineConfig([
  {
    name: 'app/files-to-lint',
    files: ['**/*.{js,mjs,jsx,vue}']
  },
  globalIgnores(['**/dist/**', '**/dist-ssr/**', '**/coverage/**']),
  js.configs.recommended,
  ...pluginVue.configs['flat/essential'],
  {
    languageOptions: {
      ecmaVersion: 'latest',
      globals: {
        ...globals.browser
      }
    }
  },
  {
    files: ['**/*.vue'],
    languageOptions: {
      parserOptions: {
        parser: tsParser
      }
    }
  },
  {
    files: ['tailwind.config.js'],
    languageOptions: {
      globals: {
        ...globals.node
      }
    }
  },
  skipFormatting
])
