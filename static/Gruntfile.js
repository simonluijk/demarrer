module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    coffee: {
      dist: {
        options: {
          join: false,
          nojoin: true,
          sourceMap: true
        },
        files: [{
          expand: true,
          cwd: 'coffee/',
          src: ['**/*.coffee'],
          dest: 'dist/js/',
          ext: '.js',
        }]
      }
    },

    concat_sourcemap: {
      dist: {
        files: {
          'dist/main.js': [
            'bower_components/jquery/jquery.js',
            'bower_components/bootstrap/js/dropdown.js',
            'dist/js/*.js'
          ]
        }
      }
    },

    uglify: {
      dist: {
        options: {
          sourceMap: 'dist/main.min.js.map',
          sourceMappingURL: 'main.min.js.map',
          sourceMapRoot: '/static/',
          sourceMapIn: 'dist/main.js.map',
        },
        files: {
          'dist/main.min.js': ['dist/main.js'],
        },
      },
    },

    less: {
      dist: {
        options: {
          compress: true
        },
        files: {
          'dist/main.min.css': 'less/main.less'
        }
      }
    },

    clean: [
      'dist/main.js',
      'dist/main.js.map',
      'dist/js/'
    ],

    watch: {
      less: {
        files: [
          'less/*.less'
        ],
        tasks: ['less']
      },
      coffee: {
        files: [
          'coffee/*.coffee'
        ],
        tasks: [
          'coffee',
          'concat_sourcemap',
          'uglify',
          'clean'
        ]
      }
    }

  });

  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-concat-sourcemap');

  grunt.registerTask('default', ['build']);
  grunt.registerTask('build', [
    'coffee',
    'concat_sourcemap',
    'uglify',
    'less',
    'clean'
  ]);

};