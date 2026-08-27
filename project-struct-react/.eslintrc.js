module.exports = {
  extends: require.resolve('@umijs/max/eslint'),
  rules: {
    // 允许 function 声明在定义前调用（函数提升），hooks 内常见写法
    '@typescript-eslint/no-use-before-define': [
      'error',
      {
        functions: false,
        classes: true,
        variables: true,
        typedefs: false,
      },
    ],
  },
};
