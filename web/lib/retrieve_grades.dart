import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:html';
import 'dart:convert';

class RetrieveGrades extends StatefulWidget {
  @override
  _RetrieveGradesState createState() => _RetrieveGradesState();
}

class _RetrieveGradesState extends State<RetrieveGrades> {
  String _subject = '';
  String _studentId = '';
  Map<String, dynamic>? _subjectGrades;
  Map<String, dynamic>? _studentGrades;

  Future<void> _getSubjectGrades() async {
    final response = await http.get(
      Uri.parse('/grades/subject/$_subject'),
    );

    if (response.statusCode == 200) {
      setState(() {
        _subjectGrades = jsonDecode(response.body);
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to retrieve grades')),
      );
    }
  }

  Future<void> _getStudentGrades() async {
    final response = await http.get(
      Uri.parse('/grades/student/$_studentId'),
    );

    if (response.statusCode == 200) {
      setState(() {
        _studentGrades = jsonDecode(response.body);
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to retrieve grades')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Retrieve Grades'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            TextFormField(
              decoration: InputDecoration(labelText: 'Subject'),
              onChanged: (value) {
                setState(() {
                  _subject = value;
                });
              },
            ),
            ElevatedButton(
              onPressed: _getSubjectGrades,
              child: Text('Get Subject Grades'),
            ),
            if (_subjectGrades != null) ...[
              Text('Number of Students: ${_subjectGrades!['num_students']}'),
              Text('Average Grade: ${_subjectGrades!['average_grade']}'),
              Text('Median Grade: ${_subjectGrades!['median_grade']}'),
            ],
            SizedBox(height: 20),
            TextFormField(
              decoration: InputDecoration(labelText: 'Student ID'),
              onChanged: (value) {
                setState(() {
                  _studentId = value;
                });
              },
            ),
            ElevatedButton(
              onPressed: _getStudentGrades,
              child: Text('Get Student Grades'),
            ),
            if (_studentGrades != null) ...[
              Text('Student ID: ${_studentGrades!['student_id']}'),
              Text('Average Grade: ${_studentGrades!['average_grade']}'),
              ..._studentGrades!['grades'].entries.map((entry) {
                return Text('${entry.key}: ${entry.value}');
              }).toList(),
            ],
          ],
        ),
      ),
    );
  }
}
