module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    meta: {
      banner: '/*! <%= pkg.name %> - v<%= pkg.version %>' + '<%= grunt.template.today("yyyy-mm-dd") %>\n' + '<%= pkg.homepage %>\n' + '* Copyright (c) <%= grunt.template.today("yyyy") %> zhyq0826: <%= pkg.author %> */\n'
    },
    concat: {
      options: {
        separator: ';'
      },
      dist: {
        // the file to concatenate
        src: [
            'js/*.js'
        ],
        // the location of the resulting js file
        dest: '../js/<%= pkg.name %>.js'
      }
    },
    uglify: {
      options: {
        // the banner is inserted at the top of the ouput
        banner: '/*! <%= pkg.name %> - v<%= pkg.version %>' + '<%= grunt.template.today("yyyy-mm-dd") %>\n' + '<%= pkg.homepage %>\n' + '* Copyright (c) <%= grunt.template.today("yyyy") %> zhyq0826: <%= pkg.author %> */\n'
      },
      dist: {
        files: {
          '../js/<%= pkg.name %>.min.js': ['<%= concat.dist.dest %>']
        }
      }
    },
    qunit: {},
    jshint: {
      all: [
          'Gruntfile.js',
          'js/*.js'
      ],
      options: {
        asi: true,
        curly: false,
        eqeqeq: true,
        eqnull: true,
        browser: true,
        globals: {
          jQuery: true
        }
      }
    },
    less: {
      production: {
        options: {
          paths: ["css/css"],
          yuicompress: true
        },
        files: {
          "../css/<%= pkg.name %>.css": "css/base.less"
        }
      }
    },
    watch: {
      css: {
        files: 'css/*.less',
        tasks: ['less'],
        options: {
          event: ['changed']
        }
      },
      scripts: {
        files: 'js/*.js',
        tasks: ['concat', 'jshint', 'uglify'],
        options: {
          event: ['changed']
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-qunit');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-less');

  //grunt.registerTask('test', ['jshint', 'qunit']);
  //grunt.registerTask('default', ['jshint', 'qunit', 'concat', 'uglify']);
  grunt.registerTask('default', ['concat', 'uglify', 'less', 'jshint'])
}