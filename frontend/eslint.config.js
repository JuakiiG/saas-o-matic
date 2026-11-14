// @ts-check
const eslint = require('@eslint/js');
const { defineConfig, globalIgnores } = require('eslint/config');
const tseslint = require('typescript-eslint');
const angular = require('angular-eslint');

// Size limits of CLAUDE.md ("Límites de tamaño"). The 250 lines per file and the 120 lines per
// `.html` template are checked by the oracle itself (scripts/oracle/checks_code.py).
const MAX_FUNCTION_LINES = 40;
const MAX_PARAMETERS = 5;
// `.claude/rules/frontend.md`: a template longer than this goes in its own `.html`.
const MAX_INLINE_TEMPLATE_LINES = 30;

module.exports = defineConfig([
  globalIgnores(['dist/', 'coverage/', '.angular/']),
  {
    files: ['**/*.ts'],
    extends: [
      eslint.configs.recommended,
      tseslint.configs.recommended,
      tseslint.configs.stylistic,
      angular.configs.tsRecommended,
    ],
    processor: angular.processInlineTemplates,
    rules: {
      'max-lines-per-function': ['error', { max: MAX_FUNCTION_LINES }],
      'max-params': ['error', { max: MAX_PARAMETERS }],
      '@angular-eslint/prefer-on-push-component-change-detection': 'error',
      '@angular-eslint/component-max-inline-declarations': [
        'error',
        { template: MAX_INLINE_TEMPLATE_LINES },
      ],
    },
  },
  {
    // The `describe` callback wraps every test of a file, so the function limit would cap the
    // number of tests per file instead of the size of each one (decision P-06, session 06).
    // The parameter limit still applies.
    files: ['**/*.spec.ts'],
    rules: { 'max-lines-per-function': 'off' },
  },
  {
    files: ['src/app/core/**/*.ts', 'src/app/shared/**/*.ts'],
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              group: ['**/features/**'],
              message: 'core/ and shared/ never import from features/.',
            },
          ],
        },
      ],
    },
  },
  {
    // Feature folders are flat (decision P-08): the only way out of one is `../../core/` or
    // `../../shared/`, so any other `../` import reaches a sibling feature.
    files: ['src/app/features/*/*.ts'],
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              regex: '^\\.\\./(?!\\.\\./(core|shared)/)',
              message: 'A feature never imports from another feature.',
            },
          ],
        },
      ],
    },
  },
  {
    files: ['**/*.html'],
    extends: [angular.configs.templateRecommended, angular.configs.templateAccessibility],
    rules: {},
  },
]);
