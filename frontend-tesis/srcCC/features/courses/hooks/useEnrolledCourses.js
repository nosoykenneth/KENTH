import { useEffect, useEffectEvent, useState } from 'react';
import { getMoodleToken, getMoodleUserId } from '@/shared/lib/moodleSession';
import { getEnrolledCourses } from '@/features/courses/services/courseService';

export default function useEnrolledCourses() {
  const [courses, setCourses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const loadCourses = useEffectEvent(async () => {
    const token = getMoodleToken();
    const userId = getMoodleUserId();

    if (!token || !userId) {
      setError('No se encontro una sesion activa.');
      setIsLoading(false);
      return;
    }

    try {
      const enrolledCourses = await getEnrolledCourses(token, userId);
      setCourses(enrolledCourses);
      setError('');
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  });

  useEffect(() => {
    loadCourses();
  }, []);

  return { courses, error, isLoading };
}
